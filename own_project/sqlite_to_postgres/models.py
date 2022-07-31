from dataclasses import dataclass, field
from datetime import datetime, date
from enum import Enum
from typing import Optional
from uuid import UUID


def _date_today():
    return datetime.date(datetime.now())


class FilmType(str, Enum):
    movie = 'movie'
    tv_show = 'tv_show'


@dataclass
class UUIDMixin:
    id: UUID


@dataclass
class TimeStampedMixin:
    created: datetime
    modified: datetime


@dataclass
class Genre(UUIDMixin, TimeStampedMixin):
    name: str
    description: Optional[str] = ""


@dataclass
class Person(UUIDMixin, TimeStampedMixin):
    full_name: str


@dataclass
class Filmwork(UUIDMixin, TimeStampedMixin):
    title: str
    type: FilmType
    creation_date: date = field(default_factory=_date_today)
    description: Optional[str] = ""
    file_path: Optional[str] = None
    rating: float = field(default=0.0)

    def __post_init__(self):
        if not self.creation_date:
            self.creation_date = _date_today()


@dataclass
class GenreFilmwork(UUIDMixin):
    film_work_id: UUID
    genre_id: UUID
    created: datetime


@dataclass
class PersonFilmwork(UUIDMixin):
    film_work_id: UUID
    person_id: UUID
    role: str
    created: datetime
