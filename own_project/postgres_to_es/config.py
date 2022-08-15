import os

from models.config import ESSettings, EtlSettings

index_names = ESSettings().indexes

_etl_settings = EtlSettings()

batch_size = _etl_settings.batch_size
es_request_timeout = _etl_settings.es_request_timeout
etl_sync_time_every_seconds = _etl_settings.etl_sync_time_every_seconds

last_state_key = _etl_settings.last_state_key

os.makedirs(_etl_settings.static_path_name, exist_ok=True)
state_file_path = os.path.abspath(_etl_settings.state_path_name)

os.makedirs(_etl_settings.static_path_name, exist_ok=True)
es_schema_path = os.path.abspath(_etl_settings.static_path_name)
