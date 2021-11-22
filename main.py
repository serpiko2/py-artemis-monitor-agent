import logging

from _agent.events.UnitCheck.RestartServiceSink import RestartServiceSink
from _agent.ServiceStatusJob import ServiceStatusSource, ServiceStatusJob
import dbus.mainloop.glib
import sys
from _agent.events.Events import Publisher
from _agent.events.UnitCheck.EventsType import EventsType
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
    pub = Publisher([EventsType.LoadStateRead, EventsType.ActiveStateRead,
                     EventsType.ExecStartInfoRead, EventsType.ReadsDone])
    status_sink = RestartServiceSink(pub, service_name)
    service_processor = ServiceStatusSource(pub)
    job = ServiceStatusJob(service_name, service_processor)
    Scheduler.schedule_jobs(job)
    Scheduler.run_loop()


    def wip():
        service_name = str(sys.argv[1]) if str(sys.argv[1]).endswith('.service') else '{0}.service'.format(
            str(sys.argv[1])) if len(sys.argv) > 2 else "artemis"
        print(f"service name: {service_name}")
        service_unit = service_name if service_name.endswith('.service') else get_sysd_object.GetUnit(
            '{0}.service'.format(service_name))
        print(f"service unit: {service_unit}")
        service_load_state = ""
        service_active_state = "active"
        if service_load_state == 'loaded' and service_active_state == 'active':
            print('service_running = True')
        else:
            print('SERVICE NOT RUN')
