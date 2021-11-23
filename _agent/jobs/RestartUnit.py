from _agent.events.Events import Publisher
from _agent.events.EventsType import EventsType
from _agent.manager import Sysd
from _agent.models.RestartServiceParameters import RestartServiceParameters
from _agent.scheduler.Job import Job


class RestartUnitJob(Job):

    def __init__(self,
                 publisher: Publisher,
                 params: RestartServiceParameters,
                 delay: int = 0,
                 loop: bool = False):
        self.publisher = publisher
        super().__init__(delay, loop, params)

    def callback(self, reply):
        self.publisher.publish(EventsType.RestartJobQueued, reply)

    def fallback(self, error):
        print(error)

    @staticmethod
    def execute(loop: bool, callback: callable, fallback: callable, params):
        print("restarting unit")
        Sysd.get_manager().RestartUnit(params.service_name,
                                       params.mode,
                                       reply_handler=callback,
                                       error_handler=fallback)
        return loop
