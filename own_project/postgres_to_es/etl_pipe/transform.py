from typing import List

from etl_pipe.etl_entities_mapping import etl_entities_mapper
from models.data import Movie, EsIndexes
from utils.backoff import backoff
from utils.logger import logger


class PGToESTransformer:
    def __init__(self, index_name: EsIndexes):
        self.index_name = index_name

    @backoff(logger=logger)
    def prepare_entries(self, data: List[tuple]) -> List[Movie]:
        """
        Преобразование списка сырых записей в список объектов модели Movie

        :param data: список записей для обработки
        :return: список объектов модели Movie
        """
        return etl_entities_mapper.get(self.index_name).prepare(data=data)

    @backoff(logger=logger)
    def compile_data(self, data: List[tuple]) -> List[dict]:
        """
        Подготовка записей для загрузки в Elasticsearch

        :param data: список записей для обработки
        :return: список подготовленных записей для загрузки в Elasticsearch
        """
        entries = self.prepare_entries(data)

        out = []
        for entry in entries:
            index_template = {
                "index": {
                    "_index": self.index_name,
                    "_id": str(entry.id)
                }
            }
            entry_template = etl_entities_mapper.get(self.index_name).entry_template(entry=entry)
            out.append(index_template)
            out.append(entry_template)

        return out
