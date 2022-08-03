from pydantic import BaseSettings, Field


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
    index: str = Field(env='ELASTIC_INDEX', default='movies')

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
    state_file_name: str = Field(env='STATE_FILE_NAME', default='last_state.json')
    static_path_name: str = Field(env='STATIC_PATH_NAME', default='static')
    es_schema_file_name: str = Field(env='ES_SCHEMA_FILE_NAME', default='es_schema.json')

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
