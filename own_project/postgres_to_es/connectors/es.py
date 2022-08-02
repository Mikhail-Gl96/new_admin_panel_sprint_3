import logging

from elasticsearch import Elasticsearch

from utils.backoff import backoff

logger = logging.getLogger(__name__)


class ElasticBase:

    def __init__(self, dsl):
        self.dsl = dsl

    @backoff(logger=logger)
    def __enter__(self):
        self.client = Elasticsearch(**self.dsl)
        print(self.client.ping())
        if not self.client.ping():
            raise ConnectionError("Elasticsearch connection error")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.transport.close()
