from abc import ABC, abstractmethod


class Job(ABC):

    def __init__(self, delay: int = 0, loop: bool = False, *params):
        self.func = self.execute
        self.delay = delay
        self.loop = loop
        self.args = (self.callback, self.fallback) + params

    def add_args(self, *args):
        self.args += args

    @abstractmethod
    def callback(self, reply):
        pass

    @abstractmethod
    def fallback(self, error):
        pass

    @staticmethod
    @abstractmethod
    def execute(loop: bool, callback: callable, fallback: callable, params):
        pass
