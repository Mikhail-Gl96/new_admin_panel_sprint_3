import datetime
from typing import Generator

from psycopg2.extensions import connection

from etl_pipe.etl_entities_mapping import etl_entities_mapper
from models.data import EsIndexes
from utils.backoff import backoff
from utils.logger import logger


class PostgresExtractor:
    def __init__(
            self,
            conn: connection,
            batch_size: int,
            index_name: EsIndexes
    ) -> None:
        self.connection = conn
        self.limit = batch_size
        self.index_name = index_name
        self.sql_query = etl_entities_mapper.get(self.index_name).sql_query

    @backoff(logger=logger)
    def get_data(
            self,
            last_update_time: datetime
    ) -> Generator[list, None, None]:
        """
        Получение данных из PostgreSQL для загрузки в ElasticSearch

        :param last_update_time: время последнего обновления данных
        :return: генератор с записями
        """

        with self.connection.cursor() as cursor:
            cursor.execute(self.sql_query % last_update_time)

            while data := cursor.fetchmany(self.limit):
                yield data
