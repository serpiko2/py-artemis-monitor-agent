import logging
import signal

import dbus.mainloop.glib

from core.manager import SystemBusSysd
from core.scheduler import Scheduler
from watchdog.AmqSyncMonitor import AmqSyncMonitor
from utils import JobsConfig, Logger, ArgParser


def exit_gracefully(*args):
    Scheduler.kill_loop()


class GracefulKiller:

    def __init__(self):
        signal.signal(signal.SIGINT, exit_gracefully)
        signal.signal(signal.SIGTERM, exit_gracefully)


def main():
    s = parser.parse_args()
    service_name = None
    mode = None
    monitor_log_path = None
    print(f"Starting monitor agent with arguments: {s}")
    logger.info(f"Starting monitor agent with arguments: {s}")
    try:
        service_name = JobsConfig.get("Jobs", "job.service.name")
        mode = JobsConfig.get("Jobs", "job.service.mode")
        monitor_log_path = JobsConfig.get("Jobs", "job.service.log_path")
    except Exception:
        pass
    print(f"Monitor for service={service_name} with mode {mode}")
    logger.info(f"Monitor for service={service_name} with mode {mode}")
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    print(f"Glib set as main loop for dbus")
    logger.info(f"Glib set as main loop for dbus")
    SystemBusSysd.get_sys_bus().add_signal_receiver(
        handler_function=lambda *args: print("received signal:", *args),
        dbus_interface=SystemBusSysd.ISYSD_PROPERTIES_STRING
    )
    if 'SYNC' == mode:
        AmqSyncMonitor(monitor_log_path, service_name)
        pass
    Scheduler.run_loop()


if __name__ == '__main__':
    killer = GracefulKiller()
    parser = ArgParser.parser
    Logger.configure_logger()
    logger = logging.getLogger("main")
    main()



