import logging

from _agent.RestartService import RestartServiceJob, RestartServiceParams
from _agent.FindService import FindUnitPropertiesJob
from _agent.events.RestartServiceSink import RestartServiceSink
import dbus.mainloop.glib
import sys
from _agent.events.Events import Publisher, Subscriber
from _agent.events.EventsType import EventsType
from _agent.events.ServiceStatusProcessor import ServiceStatusProcessor
from _agent.scheduler import Scheduler
from _utils import JobsConfig, Logger

Logger.configure_logger()
logger = logging.getLogger("main")

if __name__ == '__main__':
    logger.info("Starting monitor agent")
    service_name = JobsConfig.get("Jobs", "job.service.name")
    logger.info(f"Monitor for service={service_name}")
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    logger.info(f"Glib set as main loop for dbus")
    pub = Publisher([EventsType.RestartDone, EventsType.UnitFound])
    sub = Subscriber("find_service")
    find_unit_job = FindUnitPropertiesJob(pub, service_name)
    sub.subscribe(EventsType.RestartDone, pub,
                  callback=lambda message: Scheduler.schedule_job(find_unit_job))
    sub.subscribe(EventsType.UnitFound, pub,
                  callback=lambda message: print("found items: ", message))
    pub.publish(EventsType.RestartDone, "publish")
    restart_service_job = RestartServiceJob(
        RestartServiceParams(service_name, "replace"),
        pub
    )
    Scheduler.schedule_jobs(restart_service_job)
    Scheduler.run_loop()
#     read_properties_publisher = Publisher([EventsType.LoadStateRead, EventsType.ActiveStateRead,
#                      EventsType.ExecStartInfoRead, EventsType.ReadsDone])
#     logger.info(f"properties_publisher setup:{read_properties_publisher}")
#     unit_event_publisher = Publisher([EventsType.UnitFound, EventsType.UnitFound])
#     status_sink = RestartServiceSink(read_properties_publisher, service_name)
#     service_processor = ServiceStatusProcessor(read_properties_publisher)
#     job = ServiceStatusJob(service_name, service_processor)
#     Scheduler.schedule_jobs(job)
#     Scheduler.run_loop()


# def wip():
#     service_name = str(sys.argv[1]) if str(sys.argv[1]).endswith('.service') else '{0}.service'.format(
#         str(sys.argv[1])) if len(sys.argv) > 2 else "artemis"
#     print(f"service name: {service_name}")
#     service_unit = service_name if service_name.endswith('.service') else get_sysd_object.GetUnit(
#         '{0}.service'.format(service_name))
#     print(f"service unit: {service_unit}")
#     service_load_state = ""
#     service_active_state = "active"
#     if service_load_state == 'loaded' and service_active_state == 'active':
#         print('service_running = True')
#     else:
#         print('SERVICE NOT RUN')
