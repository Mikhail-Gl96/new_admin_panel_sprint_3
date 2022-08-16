from typing import List, Callable

from models.data import Movie, EsIndexes
from utils.backoff import backoff
from utils.logger import logger


class PGToESTransformer:
    def __init__(
            self,
            index_name: EsIndexes,
            entry_template_func: Callable,
            entry_prepare_func: Callable
    ) -> None:
        self.entry_template_func = entry_template_func
        self.index_name = index_name
        self.entry_prepare_func = entry_prepare_func

    @backoff(logger=logger)
    def prepare_entries(self, data: List[tuple]) -> List[Movie]:
        """
        Преобразование списка сырых записей в список объектов модели Movie

        :param data: список записей для обработки
        :return: список объектов модели Movie
        """
        return self.entry_prepare_func(data=data)

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
            entry_template = self.entry_template_func(entry=entry)
            out.append(index_template)
            out.append(entry_template)

        return out
