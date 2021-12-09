from abc import ABC, abstractmethod


class RegexGroup(ABC):
    """ generic group interface to represent regex search match result """
    @staticmethod
    @abstractmethod
    def build(*args):
        """"""
