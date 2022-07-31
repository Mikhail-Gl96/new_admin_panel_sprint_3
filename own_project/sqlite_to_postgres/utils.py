import collections.abc as collections_abc
import os
import sqlite3
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Optional, Any

import psycopg2.extensions as psycopg2_extensions
from dateutil.parser import parse


@contextmanager
def sqlite_conn_context(
        db_path: str
) -> collections_abc.Iterator[sqlite3.Connection]:
    conn = sqlite3.connect(db_path)
    try:
        yield conn
    finally:
        conn.close()


@dataclass
class PipelineElement:
    table: str
    model: Any
    fields_to_rename: Optional[dict] = None
    skip_empty_fields: Optional[list] = None


def load_db_envs():
    envs = {
        'dbname': os.environ.get('DB_NAME'),
        'user': os.environ.get('DB_USER'),
        'password': os.environ.get('DB_PASSWORD'),
        'host': os.environ.get('DB_HOST'),
        'port': os.environ.get('DB_PORT')
    }
    return envs


def convert_timestamp(raw_datetime: str):
    return parse(raw_datetime)


ConnectionSqlite = sqlite3.Connection
ConnectionPsycopg = psycopg2_extensions.connection

sqlite3.register_converter("timestamp", convert_timestamp)
sqlite3.register_converter("timestam", convert_timestamp)
