import signal
import dbus.mainloop.glib
from core import Logger
from core.ArgumentParser import ArgumentParser
from core.ConfigurationProperties import ConfigurationProperties
from core.Logger import get_logger
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
    print(f"Starting monitor agent with arguments: {s}")
    get_logger().info(f"Starting monitor agent with arguments: {s}")
    try:
        service_name = ConfigurationProperties.get("Jobs", "job.service.name")
        mode = ConfigurationProperties.get("Jobs", "job.service.mode")
        monitor_log_path = ConfigurationProperties.get("Jobs", "job.service.log_path")
    except ConfigurationException:
        pass
    print(f"Monitor for service={service_name} with mode {mode} and path for log {monitor_log_path}")
    get_logger().info(f"Monitor for service={service_name} with mode {mode} and path for log {monitor_log_path}")
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    print(f"Glib set as main loop for dbus")
    get_logger().info(f"Glib set as main loop for dbus")
    if 'SYNC' == mode:
        AmqMonitor(monitor_log_path, service_name)
    Scheduler.run_loop()


if __name__ == '__main__':
    killer = GracefulKiller()
    parser = ArgumentParser.get_parser()
    main()
