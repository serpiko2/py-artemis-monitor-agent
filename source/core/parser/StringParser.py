from abc import ABC, abstractmethod
from typing import Type

from source.core.parser.RegexGroup import RegexGroup


class StringParser(ABC):

    @staticmethod
    @abstractmethod
    def parse(to_parse: object, clazz: Type[RegexGroup], regex: str) -> RegexGroup:
        """ generic parse interface """
