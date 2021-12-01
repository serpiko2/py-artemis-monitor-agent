from abc import ABC, abstractmethod
from typing import Type


class Groups(ABC):
    """ generic group interface to represent regex search match result """
    @staticmethod
    @abstractmethod
    def build(*args):
        """"""


class Parser(ABC):

    @staticmethod
    @abstractmethod
    def parse(to_parse: object, clazz: Groups, regex: str) -> Groups:
        """ generic parse interface """
