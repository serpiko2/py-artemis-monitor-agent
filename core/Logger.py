import sys
from logging import handlers
import logging


class Logger:

    @staticmethod
    def get_logger(name=None, level=logging.INFO):
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(threadName) - %(levelname) - %(message)s',
                                      datefmt='%Y-%m-%d %H:%M:%S')
        handler = handlers.TimedRotatingFileHandler(filename="agent.log", when="midnight")
        handler.setFormatter(formatter)
        logger = logging.getLogger(name)
        logger.setLevel(level)
        logger.addHandler(handler)
        logger.addHandler(logging.StreamHandler(sys.stdout))
        return logger
