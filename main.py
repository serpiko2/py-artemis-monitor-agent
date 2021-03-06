from _agent.events.UnitCheck.RestartServiceSink import RestartServiceSink
from _agent.ServiceStatusJob import ServiceStatusProcessor, ServiceStatusJob
import dbus.mainloop.glib
import sys
from _agent.events.Events import Publisher
from _agent.events.UnitCheck.EventsType import EventsType
from _agent.scheduler import Scheduler
from _utils import JobsConfig


if __name__ == '__main__':
    print(JobsConfig.get("Jobs", "job.name"))
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    pub = Publisher([EventsType.LoadStateRead, EventsType.ActiveStateRead,
                     EventsType.ExecStartInfoRead, EventsType.ReadsDone])
    status_sink = RestartServiceSink(pub, "artemis.service")
    service_processor = ServiceStatusProcessor(pub)
    job = ServiceStatusJob("artemis.service", service_processor)
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
