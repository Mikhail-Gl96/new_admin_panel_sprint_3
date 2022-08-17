from typing import List, Callable, Type

from pydantic import BaseModel

from models.data import (
    EsIndexes,
    Movie,
    Genre,
    Person,
    PersonDetail,
)
from utils.sql_query import (
    all_persons,
    all_data_query,
    all_genres,
    all_detail_persons
)


class TransformMapping(BaseModel):
    prepare: Callable
    entry_template: Callable
    model: Type[BaseModel]
    sql_query: str


def prepare_movies(data: List[tuple]) -> List[Movie]:
    entries = []
    for idx, rating, genres, title, descr, director, actors_n, writers_n, actors, writers in data:
        entry = Movie(
            id=idx,
            imdb_rating=rating,
            genres=genres,
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


def prepare_persons(data: List[tuple]) -> List[Person]:
    entries = []
    for idx, full_name in data:
        entry = Person(
            id=idx,
            full_name=full_name
        )
        entries.append(entry)
    return entries


def prepare_detail_persons(data: List[tuple]) -> List[PersonDetail]:
    entries = []
    for idx, full_name, film_ids, roles in data:
        entry = PersonDetail(
            id=idx,
            full_name=full_name,
            film_ids=film_ids,
            roles=roles
        )
        entries.append(entry)
    return entries


def prepare_genres(data: List[tuple]) -> List[Genre]:
    entries = []
    for idx, name in data:
        entry = Genre(
            id=idx,
            name=name
        )
        entries.append(entry)
    return entries


def prepare_entry_movie(entry: Movie):
    return {
        "id": str(entry.id),
        "imdb_rating": entry.imdb_rating,
        "genres": entry.genres,
        "title": entry.title,
        "description": entry.description,
        "director": entry.director,
        "writers": entry.writers,
        "actors": entry.actors,
        "actors_names": entry.actors_names,
        "writers_names": entry.writers_names,
    }


def prepare_entry_detail_person(entry: Person):
    return {
        "id": str(entry.id),
        "full_name": entry.full_name
    }


def prepare_entry_full_detail_person(entry: PersonDetail):
    return {
        "id": str(entry.id),
        "full_name": entry.full_name,
        "film_ids": entry.film_ids,
        "roles": entry.roles
    }


def prepare_entry_detail_genre(entry: Genre):
    return {
        "id": str(entry.id),
        "name": entry.name
    }


etl_entities_mapper = {
    EsIndexes.movies: TransformMapping(
        prepare=prepare_movies,
        entry_template=prepare_entry_movie,
        model=Movie,
        sql_query=all_data_query
    ),
    EsIndexes.genres: TransformMapping(
        prepare=prepare_genres,
        entry_template=prepare_entry_detail_genre,
        model=Genre,
        sql_query=all_genres
    ),
    EsIndexes.persons: TransformMapping(
        prepare=prepare_persons,
        entry_template=prepare_entry_detail_person,
        model=Person,
        sql_query=all_persons
    ),
    # persons with ids and roles
    EsIndexes.persons_full: TransformMapping(
        prepare=prepare_detail_persons,
        entry_template=prepare_entry_full_detail_person,
        model=PersonDetail,
        sql_query=all_detail_persons
    ),
}
