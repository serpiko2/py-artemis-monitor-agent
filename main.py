import logging

import dbus.mainloop.glib

from _agent import Publishers
from _agent.events.Events import Publisher
from _agent.events.EventsType import EventsType
from _agent.events.UnitSignalSink import UnitSignalSink
from _agent.jobs.scheduler import Scheduler
from _agent.procedures.Procedure import Procedure
from _agent.procedures.steps.GetPropertiesStep import GetPropertiesStep
from _agent.procedures.steps.GetServiceStep import GetServiceStep
from _agent.procedures.steps.RestartUnitStep import RestartUnitStep
from _utils import JobsConfig, Logger

Logger.configure_logger()
logger = logging.getLogger("main")

if __name__ == '__main__':
    print("Starting monitor agent")
    service_name = JobsConfig.get("Jobs", "job.service.name")
    print(f"Monitor for service={service_name}")
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    print(f"Glib set as main loop for dbus")
    pub = Publisher(EventsType.Dbus.UnitRestarted, "test_publisher")
    Publishers.add_publisher("test publisher", pub)
    procedure = Procedure()
    procedure = procedure.when(
        GetServiceStep(service_name)).then(
        GetPropertiesStep()).then(
        RestartUnitStep(service_name))
    sink = UnitSignalSink(publisher=pub, callback=procedure.run())
    Scheduler.run_loop()
