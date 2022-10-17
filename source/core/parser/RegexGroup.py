from abc import ABC, abstractmethod


class RegexGroup(ABC):
    """ generic group interface to represent regex search match result """

    @classmethod
    @abstractmethod
    def build(cls, *args):
        """"""
