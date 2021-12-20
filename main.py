import signal
import dbus.mainloop.glib
from core.ArgumentParser import ArgumentParser
from core.ConfigurationProperties import ConfigurationProperties
from core.Logger import Logger
from core.scheduler.Scheduler import Scheduler
from sync.AmqMonitor import AmqMonitor


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
    logger.info(f"Starting monitor agent with arguments: {s}")
    try:
        service_name = ConfigurationProperties.get("JOBS", "job.service.name")
        mode = ConfigurationProperties.get("JOBS", "job.service.mode")
        monitor_log_path = ConfigurationProperties.get("Jobs", "job.service.log_path")
    except ConfigurationException:
        pass
    logger.info(f"Monitor for service={service_name} with mode {mode} and path for log {monitor_log_path}")
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    logger.info(f"Glib set as main loop for dbus")
    if 'SYNC' == mode:
        AmqMonitor(monitor_log_path, service_name)
    Scheduler.run_loop()


if __name__ == '__main__':
    killer = GracefulKiller()
    parser = ArgumentParser.get_parser()
    logger = Logger.get_logger('__main__')
    main()
