import logging
import signal

import dbus.mainloop.glib

from _agent import Publishers
from _agent.events.Events import Publisher
from _agent.events.EventsType import EventsType
from _agent.events.UnitSignalSink import UnitSignalSink
from _agent.manager import Sysd
from _agent.scheduler import Scheduler
from _agent.procedures.Procedure import Procedure
from _agent.procedures.steps.GetPropertiesStep import GetPropertiesStep
from _agent.procedures.steps.GetServiceStep import GetServiceStep
from _agent.procedures.steps.RestartUnitStep import RestartUnitStep
from _utils import JobsConfig, Logger, ArgParser

Logger.configure_logger()
logger = logging.getLogger("main")


def exit_gracefully(*args):
    Scheduler.kill_loop()


class GracefulKiller:

    def __init__(self):
        signal.signal(signal.SIGINT, exit_gracefully)
        signal.signal(signal.SIGTERM, exit_gracefully)


if __name__ == '__main__':
    killer = GracefulKiller()
    parser = ArgParser.parser
    s = parser.parse_args()
    service_name = None
    mode = None
    print(f"Starting monitor agent with arguments: {s}")
    logger.info(f"Starting monitor agent with arguments: {s}")
    try:
        service_name = JobsConfig.get("Jobs", "job.service.name")
        mode = JobsConfig.get("Jobs", "job.service.mode")
    except Exception:
        pass
    print(f"Monitor for service={service_name} with mode {mode}")
    logger.info(f"Monitor for service={service_name} with mode {mode}")
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    print(f"Glib set as main loop for dbus")
    logger.info(f"Glib set as main loop for dbus")
    if 'SYNC' == mode:
        pub = Publisher(EventsType.Dbus.UnitRestarted, "test_publisher")
        Publishers.add_publisher("test publisher", pub)
        procedure = Procedure()
        procedure = procedure.when(
            GetServiceStep(service_name)).then(
            GetPropertiesStep()).then(
            RestartUnitStep(service_name))
        test_procedure = Procedure().when(GetServiceStep(service_name)).run("Unit")
        print(f"test procedure result: {test_procedure}")
        procedure.run()
        Scheduler.run_loop()
        Sysd.connect_to_signal(signal="Unit", callback=procedure.run())
