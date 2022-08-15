from typing import List, Optional, Union

from pydantic import BaseSettings, Field, validator


class PostgresSettings(BaseSettings):
    dbname: str = Field(..., env='POSTGRES_DB')
    user: str = Field(..., env='POSTGRES_USER')
    password: str = Field(..., env='POSTGRES_PASSWORD')
    host: str = Field(..., env='POSTGRES_HOST')
    port: str = Field(..., env='POSTGRES_PORT')
    options: str = '-c search_path=content'

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


class ESSettings(BaseSettings):
    host: str = Field(..., env='ELASTIC_HOST')
    indexes: Union[str, List[str]] = Field(env='ELASTIC_INDEX')

    @validator('indexes', pre=True)
    def load_indexes_as_list(cls, v: Optional[str]) -> Optional[List[str]]:
        if v and isinstance(v, str):
            return [_ for _ in v.split(',') if _]
        elif v:
            raise ValueError('Incorrect indexes value')
        else:
            return None

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


class LoggerSettings(BaseSettings):
    logger_level: str = Field(env='', default='INFO')

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


class EtlSettings(BaseSettings):
    batch_size: int = Field(env='BATCH_SIZE', default=100)
    es_request_timeout: int = Field(env='ES_REQUEST_TIMEOUT', default=300)
    etl_sync_time_every_seconds: int = Field(env='ETL_SYNC_TIME_EVERY_SECONDS', default=10)
    last_state_key: str = 'last_update'

    state_path_name: str = Field(env='STATE_PATH_NAME', default='state')
    static_path_name: str = Field(env='STATIC_PATH_NAME', default='static/es_schemas')

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
