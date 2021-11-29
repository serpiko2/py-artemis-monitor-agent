from datetime import datetime

import dbus

from core.manager import SystemBusSysd
from core.scheduler import Scheduler
from watchdog.steps import MmapReadFileStep
from watchdog.steps.GetPropertiesStep import GetPropertiesStep
from watchdog.steps.GetServiceStep import GetServiceStep
from watchdog.steps.RestartUnitStep import RestartUnitStep


class AmqSyncMonitor:

    def __init__(self, logfile, service_name):
        self.logfile = logfile
        self.service_name = service_name
        try:
            self.unit = GetServiceStep.get_service(self.service_name)
        except dbus.DBusException as e:
            print("unit not found, ", e)
            Scheduler.kill_loop(1)
        self._setup_signal_sink()

    def check_from_logs(self):
        test_file = MmapReadFileStep.mmap_io_find_and_open(filename=self.logfile)
        ts = datetime.now()
        print("reading timestamp:", ts)
        for x in MmapReadFileStep.read_file(test_file, MmapReadFileStep.seek_timestamp, ts):
            return MmapReadFileStep.check_codes(x)

    def restart(self):
        unit = GetServiceStep.get_service(self.service_name)
        service_properties = GetPropertiesStep.get_service_properties(unit)
        properties = GetPropertiesStep.get_properties_for_restart(service_properties)
        restart_job = RestartUnitStep.restart_unit(properties, self.service_name)
        # reset restart counter
        return restart_job

    def start(self):
        if self.check_from_logs():
            self.restart()

    def _setup_signal_sink(self):
        print(f"unit object: {self.unit}")
        SystemBusSysd.get_sys_bus().add_signal_receiver(
            handler_function=filter_unit_signal,
            dbus_interface=SystemBusSysd.ISYSD_PROPERTIES_STRING,
            path=self.unit,
            member_keyword="PropertiesChanged"
        )


def filter_unit_signal(*args):
    print(f"received signal: {args}")
    object = args[0]
    properties = args[1]
    if object is "org.freedesktop.systemd1.Unit":
        print(f"those are the properties: {properties}")
        print(f"and since it-s an asrraay this is the first slice {properties}")
