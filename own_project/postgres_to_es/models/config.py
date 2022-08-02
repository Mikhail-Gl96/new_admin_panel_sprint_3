from pydantic import BaseSettings, Field


class PostgresSettings(BaseSettings):
    dbname: str = Field(..., env='POSTGRES_DB')
    user: str = Field(..., env='POSTGRES_USER')
    password: str = Field(..., env='POSTGRES_PASSWORD')
    host: str = Field(..., env='POSTGRES_HOST')
    port: str = Field(..., env='POSTGRES_PORT')
    options: str = '-c search_path=content'


class ESSettings(BaseSettings):
    host: str = Field(..., env='ELASTIC_HOST')
    index: str = Field(..., env='ELASTIC_INDEX')
