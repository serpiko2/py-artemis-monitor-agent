import logging
import signal

import dbus.mainloop.glib

from _agent import Publishers
from _agent.events.Events import Publisher
from _agent.events.EventsType import EventsType
from _agent.manager import SessionBusSysd
from _agent.scheduler import Scheduler
from _agent.scripts import Entrypoint
from _utils import JobsConfig, Logger, ArgParser

from gi.repository import GLib

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
        SessionBusSysd.get_sysd_proxy_object().connect_to_signal("HelloSignal", lambda m: print(m),
                                                                 arg0="Hello")
        Entrypoint.check_and_restart(service_name)
        Scheduler.run_loop()



