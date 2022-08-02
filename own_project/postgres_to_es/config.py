import os

from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')

load_dotenv(dotenv_path)

index_name = os.getenv('ELASTIC_INDEX', 'movies')

batch_size = int(os.getenv('BATCH_SIZE', 100))
es_request_timeout = int(os.getenv('ES_REQUEST_TIMEOUT', 300))
etl_sync_time_every_seconds = int(os.getenv('ETL_SYNC_TIME_EVERY_SECONDS', 10))

logger_level = os.getenv('LOGGER_LEVEL', 'INFO')

last_state_key = 'last_update'

os.makedirs('state', exist_ok=True)
state_file_path = os.path.abspath(os.path.join('state', 'last_state.json'))

os.makedirs('static', exist_ok=True)
es_schema_path = os.path.abspath(os.path.join('static', 'es_schema.json'))
