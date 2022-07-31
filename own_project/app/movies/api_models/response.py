from datetime import date
from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel, validator, Field


class Movie(BaseModel):
    id: UUID
    title: str
    description: str
    creation_date: date
    rating: Optional[float]
    type: str
    genres: List[str] = Field(alias='genre')
    actors: List[str]
    directors: List[str]
    writers: List[str]

    @validator('description', pre=True, allow_reuse=True)
    def _check_desc(cls, v: Optional[str]):
        if not v:
            v = ''
        return v


class MovieResponse(BaseModel):
    count: int
    total_pages: int
    prev: Optional[int]
    next: Optional[int]
    results: List[Movie]
