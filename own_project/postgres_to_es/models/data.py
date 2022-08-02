from uuid import UUID

from pydantic import BaseModel, validator, Field
from pydantic.schema import Optional, List, Any, Dict


class Person(BaseModel):
    id: str
    name: str


class Movie(BaseModel):
    id: UUID
    imdb_rating: Optional[float] = Field(alias='rating')
    genre: Optional[List[str]]
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
                Person(**i)

    @validator('imdb_rating')
    def valid_imdb_rating(cls, v: Optional[Any]):
        return cls._return_default_if_empty(v, 0)

    @validator('description')
    def valid_description(cls, v: Optional[Any]):
        return cls._return_default_if_empty(v, '')

    @validator('director')
    def valid_director(cls, v: Optional[Any]):
        return cls._return_default_if_empty(v, [])

    @validator('actors')
    def valid_actors(cls, v: Optional[Any]):
        cls.validate_person_list(v)
        return cls._return_default_if_empty(v, [])

    @validator('writers')
    def valid_writers(cls, v: Optional[Any]):
        cls.validate_person_list(v)
        return cls._return_default_if_empty(v, [])

    @validator('actors_names')
    def valid_actors_names(cls, v: Optional[Any]):
        return cls._return_default_if_empty(v, [])

    @validator('writers_names')
    def valid_writers_names(cls, v: Optional[Any]):
        return cls._return_default_if_empty(v, [])
