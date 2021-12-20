import sys
from logging import handlers
import logging


class Logger:

    @staticmethod
    def get_logger(name=None, level=logging.INFO):
        formatter = logging.Formatter('%(asctime)s [%(name)s] [%(threadName)] [%(levelname)] - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        handler = handlers.TimedRotatingFileHandler(filename="agent.log", when="midnight")
        handler.setFormatter(formatter)
        logger = logging.getLogger(name)
        logger.setLevel(level)
        logger.addHandler(handler)
        logger.addHandler(logging.StreamHandler(sys.stdout))
        return logger


class Loggable:
    def __call__(self, f):
        def wrap(init_self, *args, **kwargs):
            init_self.logger = Logger.get_logger(init_self.__class__.__name__)
            f(init_self, *args, **kwargs)
        return wrap
