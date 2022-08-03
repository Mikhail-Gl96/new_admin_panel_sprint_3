import logging

from models.config import LoggerSettings

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.getLevelName(LoggerSettings().logger_level))
