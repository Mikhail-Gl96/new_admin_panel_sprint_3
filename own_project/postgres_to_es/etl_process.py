import os.path
import time
from contextlib import contextmanager
from typing import Generator

import elasticsearch
import psycopg2
from elasticsearch.client import Elasticsearch
from psycopg2.extensions import connection

from config import (
    index_names,
    es_schema_path,
    state_file_path,
    last_state_key,
    batch_size,
    es_request_timeout,
    etl_sync_time_every_seconds
)
from etl_pipe.etl_entities_mapping import etl_entities_mapper
from etl_pipe.extract import PostgresExtractor
from etl_pipe.load import ESLoader
from etl_pipe.transform import PGToESTransformer
from models.config import ESSettings, PostgresSettings
from models.data import EsIndexes
from utils.backoff import backoff
from utils.logger import logger
from utils.state import JsonFileStorage, State


def operations_index_not_exists(
        loader: ESLoader,
        state: State,
        index_name: EsIndexes
) -> None:
    logger.info(f'No index <{index_name}>. Try to create one.')
    loader.create_index()
    logger.info(f'Index <{index_name}> created. Start clear state.')
    state.set_state(last_state_key, None)
    logger.info('State cleared')


def run_etl_process_per_index(
        pg_conn: connection,
        es_conn: Elasticsearch,
        index_name: EsIndexes,
        state_file_path: str
) -> None:
    storage = JsonFileStorage(state_file_path)
    state = State(storage)

    sql_query = etl_entities_mapper.get(index_name).sql_query
    extractor = PostgresExtractor(
        conn=pg_conn,
        batch_size=batch_size,
        sql_query=sql_query
    )

    entry_template_func = etl_entities_mapper.get(index_name).entry_template
    entry_prepare_func = etl_entities_mapper.get(index_name).prepare
    transformer = PGToESTransformer(
        index_name=index_name,
        entry_template_func=entry_template_func,
        entry_prepare_func=entry_prepare_func
    )

    es_schema_path_by_index = os.path.join(es_schema_path, f'{index_name}.json')
    loader = ESLoader(
        connection=es_conn,
        index_name=index_name,
        es_schema_path=es_schema_path_by_index
    )

    if not es_conn.indices.exists(index=index_name):
        operations_index_not_exists(
            loader=loader,
            state=state,
            index_name=index_name
        )

    last_update_time = state.get_state(last_state_key)
    pg_data = extractor.get_data(last_update_time)

    for batch in pg_data:
        entries = transformer.compile_data(batch)
        loader.bulk_create(entries, state)


def main() -> None:
    with closing_es(connect_es()) as es_conn, closing(connect_postgres()) as pg_conn:
        for _index_name in index_names:
            _state_file_path = os.path.join(state_file_path, f'last_state_{_index_name}.json')
            run_etl_process_per_index(
                pg_conn=pg_conn,
                es_conn=es_conn,
                index_name=_index_name,
                state_file_path=_state_file_path
            )


@contextmanager
def closing(smth) -> Generator:
    try:
        yield smth
    finally:
        smth.close()


@contextmanager
def closing_es(es_client) -> Generator:
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
