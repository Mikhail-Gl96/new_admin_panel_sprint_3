import time
from contextlib import contextmanager

import elasticsearch
import psycopg2
from elasticsearch.client import Elasticsearch
from psycopg2.extensions import connection

from config import (
    index_name,
    state_file_path,
    last_state_key,
    batch_size,
    es_request_timeout,
    etl_sync_time_every_seconds
)
from etl_pipe.extract import PostgresExtractor
from etl_pipe.load import ESLoader
from etl_pipe.transform import PGToESTransformer
from models.config import ESSettings, PostgresSettings
from utils.backoff import backoff
from utils.logger import logger
from utils.state import JsonFileStorage, State


def main() -> None:
    with closing_es(connect_es()) as es_conn, closing(connect_postgres()) as pg_conn:
        storage = JsonFileStorage(state_file_path)
        state = State(storage)
        extractor = PostgresExtractor(pg_conn, batch_size)
        transformer = PGToESTransformer()
        loader = ESLoader(es_conn, index_name)

        if not es_conn.indices.exists(index=index_name):
            logger.info(f'No index <{index_name}>. Try to create one.')
            # Я бы оставил, тк индекс может быть затерт (случай, конечно, нестандартный).
            # Если во время сканирования поймем, что индекса нет - пересоздадим.
            # И стейт почистим, чтобы все загрузить заново. Либо нужно создавать отд процесс (демон, сервис),
            # который будет следить за состоянием накачки данных и сохранностью индексов.
            loader.create_index()
            logger.info(f'Index <{index_name}> created. Start clear state.')
            state.set_state(last_state_key, None)
            logger.info('State cleared')

        last_update_time = state.get_state(last_state_key)
        pg_data = extractor.get_data(last_update_time)

        for batch in pg_data:
            entries = transformer.compile_data(batch)
            loader.bulk_create(entries, state)


@contextmanager
def closing(smth):
    try:
        yield smth
    finally:
        smth.close()


@contextmanager
def closing_es(es_client):
    try:
        yield es_client
    finally:
        es_client.transport.close()


@backoff(logger=logger)
def connect_es() -> Elasticsearch:
    """
    Подключение к Elasticsearch

    :return: Клиент соединения Elastic
    """

    es_conn = elasticsearch.Elasticsearch(
        hosts=[ESSettings().host],
        request_timeout=es_request_timeout
    )
    return es_conn


@backoff(logger=logger)
def connect_postgres() -> connection:
    """
    Подключение к PostgreSQL

    :return: Клиент соединения Postgres
    """
    pg_conn = psycopg2.connect(**PostgresSettings().dict())
    return pg_conn


if __name__ == '__main__':
    logger.info('Start ETL process')
    while True:
        main()
        logger.debug('Time to sleep')
        time.sleep(etl_sync_time_every_seconds)
        logger.debug('Continue sync')
