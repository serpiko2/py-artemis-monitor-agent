from abc import ABC, abstractmethod


class Job(ABC):

    def __init__(self, delay: int = 0, loop: bool = False, *params):
        """ The Job abstract class, every job that needs to be run by the scheduler extends this class
            :params:
                `delay`:`the delay to run the job in milliseconds`
                `loop`:`true to make it loop every delay_time, false to not (deterministic jobs don't support this)`
                `*params`:`the job parameters - for now it will add the callback and fallback to this object`
        """

        self.func = self.execute
        self.delay = delay
        self.loop = loop
        self.args = (self.callback, self.fallback) + params

    @abstractmethod
    def callback(self, reply):
        """ the callback to be executed
            :param:
                `reply`:`the reply`
         """
    @abstractmethod
    def fallback(self, error):
        """ the callback to be executed
            :param:
                `error`:`the error reply`
        """
    @staticmethod
    @abstractmethod
    def execute(loop: bool, callback: callable, fallback: callable, params):
        """ the entrypoint for the job, the scheduler will run it on the event loop,
         it has to be non blocking or you have to delegate it to a secondary thread pool executor
            :param:
                `loop`:`true or false to make it loop, ignore if the job is deterministic`
                `callback`:`the callback to be executed to handle the non blocking function response`
                `fallback`:`the fallback to be executed to handle the non blocking function error`
                `params`:`an object that holds the parameters for the function to run`
        """