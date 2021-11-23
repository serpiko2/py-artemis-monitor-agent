from _agent.events.Events import Subscriber
from _agent.events.EventsType import EventsType
from _agent.scheduler import schedule_job


class RestartServiceSink:

    def __init__(self, publisher, service_name, name='RestartServiceSink'):
        job = RestartServiceJob.RestartServiceJob(service_name)
        properties_listener = Subscriber(name)
        properties_listener.subscribe(EventsType.UnitFound, publisher,
                                      callback=lambda message: schedule_job(job))
