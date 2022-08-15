from enum import Enum
from uuid import UUID

from pydantic import BaseModel, validator, Field
from pydantic.schema import Optional, List, Any, Dict


class EsIndexes(str, Enum):
    movies = 'movies'
    persons = 'persons'
    genres = 'genres'
    persons_full = 'persons_full'

    @staticmethod
    def members():
        return list(EsIndexes)


class IdNameMixin(BaseModel):
    id: str
    name: str


class Genre(IdNameMixin):
    description: Optional[str]


class Person(BaseModel):
    id: str
    full_name: str = Field(alias='name')

    class Config:
        allow_population_by_field_name = True


class PersonDetail(Person):
    film_ids: Optional[List[str]]
    roles: Optional[List[str]]

    @validator('film_ids', pre=True)
    def validate_film_ids(cls, v: Optional[str]) -> Optional[List[str]]:
        if v and isinstance(v, str):
            return v.replace('{', '').replace('}', '').split(',')
        return None


class Movie(BaseModel):
    id: UUID
    imdb_rating: Optional[float] = Field(alias='rating')
    genres: Optional[List[Dict[str, str]]]
    title: str
    description: Optional[str]
    director: Optional[List[str]]
    actors: Optional[List[Dict[str, str]]]
    writers: Optional[List[Dict[str, str]]]
    actors_names: Optional[List[str]]
    writers_names: Optional[List[str]]

    class Config:
        allow_population_by_field_name = True

    @staticmethod
    def _return_default_if_empty(v, default: Any) -> Optional[Any]:
        if v is None:
            return default
        return v

    @staticmethod
    def validate_person_list(v: list):
        if v:
            for i in v:
                IdNameMixin(**i)

    @validator('imdb_rating')
    def valid_imdb_rating(cls, v: Optional[Any]):
        return cls._return_default_if_empty(v, 0)

    @validator('description')
    def valid_description(cls, v: Optional[Any]):
        return cls._return_default_if_empty(v, '')

    @validator('director')
    def valid_director(cls, v: Optional[Any]):
        return cls._return_default_if_empty(v, [])

    @validator('actors', 'writers', 'genres')
    def valid_actors(cls, v: Optional[Any]):
        cls.validate_person_list(v)
        return cls._return_default_if_empty(v, [])

    @validator('actors_names')
    def valid_actors_names(cls, v: Optional[Any]):
        return cls._return_default_if_empty(v, [])

    @validator('writers_names')
    def valid_writers_names(cls, v: Optional[Any]):
        return cls._return_default_if_empty(v, [])
