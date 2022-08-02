import logging
import time
from typing import Tuple

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
    etl_sync_time_every_seconds,
    logger_level
)
from etl_pipe.extract import PostgresExtractor
from etl_pipe.load import ESLoader
from etl_pipe.transform import PGToESTransformer
from models.config import ESSettings, PostgresSettings
from utils.backoff import backoff
from utils.state import JsonFileStorage, State

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.getLevelName(logger_level))


def main() -> None:
    es_conn, pg_conn = connect()
    storage = JsonFileStorage(state_file_path)
    state = State(storage)
    extractor = PostgresExtractor(pg_conn, batch_size)
    transformer = PGToESTransformer()
    loader = ESLoader(es_conn, index_name)

    if not es_conn.indices.exists(index=index_name):
        loader.create_index()

    last_update_time = state.get_state(last_state_key)
    pg_data = extractor.get_data(last_update_time)

    for batch in pg_data:
        entries = transformer.compile_data(batch)
        loader.bulk_create(entries, state)


@backoff(logger=logger)
def connect() -> Tuple[Elasticsearch, connection]:
    """
    Подключение к Elasticsearch и PostgreSQL

    :return: Клиенты соединений Postgre и Elastic
    """
    es_conn = elasticsearch.Elasticsearch(
        hosts=[ESSettings().host],
        request_timeout=es_request_timeout
    )
    pg_conn = psycopg2.connect(**PostgresSettings().dict())
    return es_conn, pg_conn


if __name__ == '__main__':
    logger.info('Start ETL process')
    while True:
        main()
        logger.debug('Time to sleep')
        time.sleep(etl_sync_time_every_seconds)
        logger.debug('Continue sync')
