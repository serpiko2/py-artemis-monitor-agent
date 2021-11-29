from agent.events.Events import Publisher
from agent.events.EventsType import EventsType
from core.manager import SystemBusSysd
from agent.models.RestartServiceParameters import RestartServiceParameters
from async import Job


class RestartUnitJob(Job):

    @staticmethod
    def execute(loop: bool, callback: callable, fallback: callable, params):
        SystemBusSysd.get_sysd_manager().RestartUnit(params.service_name,
                                                     params.mode,
                                                     reply_handler=callback,
                                                     error_handler=fallback)
        return loop

    def __init__(self,
                 publisher: Publisher,
                 params: RestartServiceParameters,
                 delay: int = 0,
                 loop: bool = False):
        self.publisher = publisher
        super().__init__(delay, loop, params)

    def callback(self, reply):
        self.publisher.publish(EventsType.Jobs.RestartJobQueued, reply)

    def fallback(self, error):
        print(error)
