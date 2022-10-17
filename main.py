import dbus.mainloop.glib
import logging

from source.asyn.handlers.DbusSignalHandler import DbusSignalHandler
from source.asyn.handlers.JobsEventHandler import JobsEventHandler
from source.asyn.handlers.MonitorEventHandler import MonitorEventHandler
from source.config.MonitorConfig import MonitorConfig
from source.utils.ArgumentParser import ArgumentParser
from source.utils.Logger import Logger
from source.core.scheduler.Scheduler import Scheduler


class ConfigurationException(Exception):
    """"""


def main():
    logging.info(f"Starting monitor agent with arguments: {parser}")
    logging.info(f"Monitor for service={MonitorConfig.service_name} and path for log {MonitorConfig.file_path}")
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    logging.info(f"Glib set as main loop for dbus")
    DbusSignalHandler()
    JobsEventHandler()
    MonitorEventHandler()
    Scheduler.run_loop()


if __name__ == '__main__':
    parser = ArgumentParser.get_parsed_args()
    logger = Logger.get_logger()
    main()
