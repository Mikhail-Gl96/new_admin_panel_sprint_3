import abc
import datetime
import json
import os
from typing import Any, Optional


class BaseStorage:
    @abc.abstractmethod
    def save_state(self, state: dict) -> None:
        """Сохранить состояние в постоянное хранилище"""
        pass

    @abc.abstractmethod
    def retrieve_state(self) -> dict:
        """Загрузить состояние локально из постоянного хранилища"""
        pass


class JsonFileStorage(BaseStorage):
    def __init__(self, file_path: Optional[str] = None):
        self.file_path = file_path

    @staticmethod
    def _read_json_file(file_path) -> dict:
        with open(file_path, 'r') as f:
            return json.loads(f.read())

    def retrieve_state(self) -> dict:
        if os.path.exists(self.file_path):
            possible_state = self._read_json_file(self.file_path)
            return possible_state if possible_state else {}
        return {}

    def save_state(self, state: dict) -> None:
        with open(self.file_path, 'w') as f:
            f.write(json.dumps(state))


class State:
    """
    Класс для хранения состояния при работе с данными, чтобы постоянно не перечитывать данные с начала.
    Здесь представлена реализация с сохранением состояния в файл.
    В целом ничего не мешает поменять это поведение на работу с БД или распределённым хранилищем.
    """

    def __init__(self, storage: BaseStorage):
        self.storage = storage

    def set_state(self, key: str, value: Any) -> None:
        self.storage.save_state({key: value})

    def get_state(self, key: str) -> Any:
        state = self.storage.retrieve_state()
        state_by_key = state.get(key)
        return state_by_key if state_by_key else datetime.datetime.min
