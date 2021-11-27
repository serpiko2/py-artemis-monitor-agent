from _agent.events.Events import Publisher
from _agent.events.EventsType import EventsType
from _agent.models.PropertiesServiceParameters import PropertiesServiceParameters
from _agent.scheduler.Job import Job


class Interfaces:
    Unit = 'org.freedesktop.systemd1.Unit'
    Service = 'org.freedesktop.systemd1.Service'


class Properties:
    ActiveState = 'ActiveState'
    LoadState = 'LoadState'
    ExecStart = 'ExecStart'


class GetPropertyJob(Job):

    @staticmethod
    def execute(loop: bool, callback: callable, fallback: callable, params: PropertiesServiceParameters):
        """ Unimplemented job stub - use this as a reference structure
        """
        params.service_properties.Get(
            params.interface, params.name,
            reply_handler=callback,
            error_handler=fallback
        )
        # return false to not loop
        return loop

    def __init__(self,
                 publisher: Publisher,
                 event: EventsType,
                 params: PropertiesServiceParameters,
                 delay: int = 0,
                 loop=False):
        super().__init__(delay, loop, params)
        self.publisher = publisher
        self.event = event

    def callback(self, reply):
        self.publisher.publish(self.event, reply)

    def fallback(self, error):
        print(f"{error}")
