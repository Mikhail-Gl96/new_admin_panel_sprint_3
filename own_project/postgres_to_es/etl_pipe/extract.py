import datetime
import logging
from typing import Generator

from psycopg2.extensions import connection

from utils.backoff import backoff
from utils.sql_query import all_data_query

logger = logging.getLogger(__name__)


class PostgresExtractor:
    def __init__(self, conn: connection, batch_size: int) -> None:
        self.connection = conn
        self.limit = batch_size

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

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(all_data_query % last_update_time)

                while data := cursor.fetchmany(self.limit):
                    yield data

        except Exception as error:
            logger.error(error)
