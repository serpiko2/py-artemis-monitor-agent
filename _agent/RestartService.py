from _agent.events.EventsType import EventsType
from _agent.manager import Sysd
from _agent.scheduler.Scheduler import Job


class RestartServiceParams:

    def __init__(self,
                 service_name: str,
                 mode: str = 'replace'):
        self.service_name = service_name
        self.mode = mode


class RestartServiceJob(Job):

    def __init__(self,
                 params: RestartServiceParams,
                 publisher,
                 delay: int = 0,
                 loop: bool = False):
        print("init service")
        super().__init__(_restart_unit, delay, loop, params)
        self.params = params
        self.publisher = publisher

    def callback(self, reply):
        self.publisher.publish(EventsType.RestartDone, reply)

    def fallback(self, error):
        print(error)


def _restart_unit(loop: bool, callback: callable, fallback: callable, params):
    print("restarting unit")
    Sysd.get_manager().RestartUnit(params.service_name,
                                   params.mode,
                                   reply_handler=callback,
                                   error_handler=fallback)
    return loop


