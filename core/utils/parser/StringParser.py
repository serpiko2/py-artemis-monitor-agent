import re
from abc import ABC, abstractmethod
from typing import Type


class Groups(ABC):
    """ generic group to represent regex search match result """
    @staticmethod
    @abstractmethod
    def build(*args):
        """"""


class Parser(ABC):
    @staticmethod
    def parse_string(line, clazz: Type[Groups], regex: str) -> Groups:
        groups = re.search(regex, line).groups()
        return clazz.build(*groups)

