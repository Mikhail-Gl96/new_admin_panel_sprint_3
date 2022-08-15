import datetime
from typing import List

from elasticsearch.client import Elasticsearch

from config import last_state_key
from utils.backoff import backoff
from utils.logger import logger
from utils.state import State


class ESLoader:
    def __init__(
            self,
            connection: Elasticsearch,
            index_name: str,
            es_schema_path: str
    ) -> None:
        self.es_conn = connection
        self.index_name = index_name
        self.es_schema_path = es_schema_path

    @backoff(logger=logger)
    def create_index(self) -> None:
        """
        Создание индекса
        :return: None
        """
        with open(self.es_schema_path, 'r') as file:
            data = file.read()

        self.es_conn.indices.create(index=self.index_name, body=data)
        logger.info('Index created')

    @backoff(logger=logger)
    def bulk_create(
            self,
            entries: List[dict],
            state: State
    ) -> None:
        """
        Массовое создание документов в Elasticsearch

        :param entries: список записей в виде объектов модели Movie
        :param state: объект класса State для хранения состояний
        :return: None
        """
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        state.set_state(last_state_key, now)

        self.es_conn.bulk(index=self.index_name, body=entries)
