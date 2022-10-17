from logging import handlers
import logging

from source.utils.ConfigurationProperties import ConfigurationProperties


class Logger:

    log_mapping = {"INFO": 20, "DEBUG": 10, "WARN": 30, "ERROR": 40, "CRITICAL": 50}
    _log_level = log_mapping.get(ConfigurationProperties.get('LOGGER', 'logger.level'))
    _log_file = ConfigurationProperties.get('LOGGER', 'logger.file')

    @staticmethod
    def get_logger(level=_log_level):
        formatter = logging.Formatter('[%(asctime)s] - [%(name)s] - [%(threadName)s] - [%(levelname)s] - %(message)s',
                                      datefmt='%Y-%m-%d %H:%M:%S')
        handler = handlers.TimedRotatingFileHandler(filename=Logger._log_file, when="midnight")
        handler.setLevel(level)
        handler.setFormatter(formatter)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        logger = logging.getLogger()
        logger.setLevel(level)
        logger.addHandler(handler)
        logger.addHandler(console_handler)