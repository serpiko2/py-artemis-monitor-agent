import logging
import signal

import dbus.mainloop.glib

from core.scheduler import Scheduler
from core.utils import Logger
from core.utils.ArgumentParser import ArgumentParser
from core.utils.ConfigurationProperties import ConfigurationProperties
from sync.AmqSyncMonitor import AmqSyncMonitor
from sync.steps.GetServiceStep import GetServiceStep


def exit_gracefully(*args):
    Scheduler.kill_loop()


class GracefulKiller:

    def __init__(self):
        signal.signal(signal.SIGINT, exit_gracefully)
        signal.signal(signal.SIGTERM, exit_gracefully)


class ConfigurationException(Exception):
    """"""


def main():
    s = parser.parse_args()
    service_name = None
    mode = None
    monitor_log_path = None
    print(f"Starting monitor agent with arguments: {s}")
    logger.info(f"Starting monitor agent with arguments: {s}")
    try:
        service_name = ConfigurationProperties.get("Jobs", "job.service.name")
        mode = ConfigurationProperties.get("Jobs", "job.service.mode")
        monitor_log_path = ConfigurationProperties.get("Jobs", "job.service.log_path")
    except ConfigurationException:
        pass
    print(f"Monitor for service={service_name} with mode {mode} and path for log {monitor_log_path}")
    logger.info(f"Monitor for service={service_name} with mode {mode}")
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    print(f"Glib set as main loop for dbus")
    logger.info(f"Glib set as main loop for dbus")
    print(GetServiceStep.get_service(service_name))
    if 'SYNC' == mode:
        AmqSyncMonitor(monitor_log_path, service_name)
        pass
    Scheduler.run_loop()


if __name__ == '__main__':
    killer = GracefulKiller()
    parser = ArgumentParser.get_parser()
    Logger.configure_logger()
    logger = logging.getLogger("main")
    main()
