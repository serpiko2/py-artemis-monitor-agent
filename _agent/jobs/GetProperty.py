from _agent.events.Events import Publisher
from _agent.events.EventsType import EventsType
from _agent.models.PropertiesServiceParameters import PropertiesServiceParameters
from _agent.scheduler.Job import Job


class GetPropertyJob(Job):

    def __init__(self,
                 publisher: Publisher,
                 event: EventsType,
                 params: PropertiesServiceParameters,
                 delay: int = 0,
                 loop=False):
        super().__init__(GetPropertyJob.execute, delay, loop, params)
        self.publisher = publisher
        self.event = event

    def callback(self, reply):
        self.publisher.publish(self.event, reply.data)

    def fallback(self, error):
        print(f"{error}")

    @staticmethod
    def execute(loop: bool, callback: callable, fallback: callable, params: PropertiesServiceParameters):
        """entry_point placeholder.
        """
        params.service_properties.Get(
            params.interface, params.name,
            reply_handler=lambda message: callback,
            error_handler=fallback
        )
        # return false to not loop
        return loop
