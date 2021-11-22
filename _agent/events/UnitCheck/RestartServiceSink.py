from _agent.RestartServiceJob import RestartServiceJob
from _agent.events.Events import Subscriber
from _agent.events.UnitCheck.EventsType import EventsType

class RestartServiceSink:

    def __init__(self, publisher, service_name, name='RestartServiceSink'):
        job = RestartServiceJob(service_name)
        properties_listener = Subscriber(name)
        properties_listener.subscribe(EventsType.ReadsDone, publisher,
                                      callback=lambda message:job.check_status(message))


