from abc import ABC, abstractmethod


class Step(ABC):

    @abstractmethod
    def __init__(self, **params):
        """"""

    @abstractmethod
    def apply(self, **params):
        """ the entrypoint for the step, the scheduler will run it on the event loop,
         it has to be non blocking or you have to delegate it to a secondary thread pool executor
            :param:
                `loop`:`true or false to make it loop, ignore if the job is deterministic`
                `callback`:`the callback to be executed to handle the non blocking function response`
                `fallback`:`the fallback to be executed to handle the non blocking function error`
                `params`:`an object that holds the parameters for the function to run`
        """

    def before(self, *params):
        return params

    def after(self, *params):
        """"""
        return params
