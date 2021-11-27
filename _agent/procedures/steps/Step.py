from abc import ABC, abstractmethod
from typing import overload


class Step(ABC):

    @abstractmethod
    def __init__(self, **args):
        """"""

    @abstractmethod
    @overload
    def apply(self):
        """ the entrypoint for the step, the scheduler will run it on the event loop,
         it has to be non blocking or you have to delegate it to a secondary thread pool executor
            :param:
                `loop`:`true or false to make it loop, ignore if the job is deterministic`
                `callback`:`the callback to be executed to handle the non blocking function response`
                `fallback`:`the fallback to be executed to handle the non blocking function error`
                `params`:`an object that holds the parameters for the function to run`
        """

    @abstractmethod
    def apply(self, **args):
        """ the entrypoint for the step, the scheduler will run it on the event loop,
         it has to be non blocking or you have to delegate it to a secondary thread pool executor
            :param:
                `loop`:`true or false to make it loop, ignore if the job is deterministic`
                `callback`:`the callback to be executed to handle the non blocking function response`
                `fallback`:`the fallback to be executed to handle the non blocking function error`
                `params`:`an object that holds the parameters for the function to run`
        """

    @overload
    def before(self):
        print(f"BEFORE.self:{self}, args:NO_ARGS")
        pass

    def before(self, **args):
        print(f"BEFORE.self:{self}, args:{args}")
        return args

    @overload
    def after(self):
        print(f"AFTER.self:{self}, args:NO_ARGS")
        pass

    def after(self, *args):
        print(f"AFTER.self:{self}, args:{args}")
        return args
