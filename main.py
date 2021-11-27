import logging

import dbus.mainloop.glib

from _agent import Publishers
from _agent.events.Events import Publisher, Subscriber
from _agent.events.EventsType import EventsType, get_events
from _agent.events.StatusAwareProcessor import StatusAwareProcessor
from _agent.jobs.GetService import FindPropertiesJob
from _agent.jobs.RestartUnit import RestartUnitJob
from _agent.models.RestartServiceParameters import RestartServiceParameters
from _agent.scheduler import Scheduler
from _utils import JobsConfig, Logger

Logger.configure_logger()
logger = logging.getLogger("main")

if __name__ == '__main__':
    print("Starting monitor agent")
    service_name = JobsConfig.get("Jobs", "job.service.name")
    print(f"Monitor for service={service_name}")
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    print(f"Glib set as main loop for dbus")
    pub = Publisher(get_events(), "test_publisher")
    Publishers.add_publisher("test publisher", pub)
    sub = Subscriber("find_service")
    sub.subscribe(EventsType.RestartJobQueued, Publishers.get_publisher("test publisher"), callback=lambda reply:
                  print(reply, EventsType.RestartJobQueued))
    params = RestartServiceParameters(service_name)
    restart_job = RestartUnitJob(params=params,
                                 publisher=Publishers.get_publisher("test publisher"))
    processor = StatusAwareProcessor(publisher=Publishers.get_publisher("test publisher"),
                                     listener=sub,
                                     service_name=service_name)
    get_service_job = FindPropertiesJob(service_name=service_name,
                                        publisher=pub)
    Scheduler.schedule_job(get_service_job)
    Scheduler.run_loop()
