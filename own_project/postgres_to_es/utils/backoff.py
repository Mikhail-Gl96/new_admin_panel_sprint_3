from functools import wraps
from time import sleep
from typing import Callable

from utils.logger import logger


def backoff(
        start_sleep_time: float = 0.1,
        factor: int = 2,
        border_sleep_time: float = 10,
        logger: logger = logger,
) -> Callable:
    """
    Функция для повторного выполнения функции через некоторое время,
    если возникла ошибка. Использует наивный экспоненциальный рост времени
    повтора (factor) до граничного времени ожидания (border_sleep_time)
    Формула:
        t = start_sleep_time * 2^(n) if t < border_sleep_time
        t = border_sleep_time if t >= border_sleep_time
    :param start_sleep_time: начальное время повтора
    :param factor: во сколько раз нужно увеличить время ожидания
    :param border_sleep_time: граничное время ожидания
    :param logger: логгер
    :return: результат выполнения функции
    """

    def func_wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            n = 0
            while True:
                sleep_time = start_sleep_time * factor ** n
                try:
                    result = func(*args, **kwargs)
                    n = 0  # сброс счетчика накрутки если все удачно
                    return result
                except Exception as err:
                    logger.error(
                        f'Error in <{func.__name__}>. Error: {err}'
                    )
                    if sleep_time >= border_sleep_time:
                        sleep_time = border_sleep_time
                    else:
                        n += 1
                    logger.info(f'reconnect again after {sleep_time} seconds')
                    sleep(sleep_time)
                    logger.info('reconnecting ...')

        return inner

    return func_wrapper
