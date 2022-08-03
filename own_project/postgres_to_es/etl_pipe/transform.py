from typing import List

from config import index_name
from models.data import Movie
from utils.backoff import backoff
from utils.logger import logger


class PGToESTransformer:
    @backoff(logger=logger)
    def prepare_entries(self, data: List[tuple]) -> List[Movie]:
        """
        Преобразование списка сырых записей в список объектов модели Movie

        :param data: список записей для обработки
        :return: список объектов модели Movie
        """
        entries = []
        for idx, rating, genre, title, descr, director, actors_n, writers_n, actors, writers in data:
            entry = Movie(
                id=idx,
                imdb_rating=rating,
                genre=genre,
                title=title,
                description=descr,
                director=director,
                actors=actors,
                writers=writers,
                actors_names=actors_n,
                writers_names=writers_n
            )
            entries.append(entry)
        return entries

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
                    "_index": index_name,
                    "_id": str(entry.id)
                }
            }
            entry_template = {
                "id": str(entry.id),
                "imdb_rating": entry.imdb_rating,
                "genre": entry.genre,
                "title": entry.title,
                "description": entry.description,
                "director": entry.director,
                "writers": entry.writers,
                "actors": entry.actors,
                "actors_names": entry.actors_names,
                "writers_names": entry.writers_names,
            }
            out.append(index_template)
            out.append(entry_template)

        return out
