from datetime import datetime

from core.manager import SystemBusSysd
from watchdog.steps import MmapReadFileStep
from watchdog.steps.GetPropertiesStep import GetPropertiesStep
from watchdog.steps.GetServiceStep import GetServiceStep
from watchdog.steps.RestartUnitStep import RestartUnitStep


class AmqSyncMonitor:

    def __init__(self, logfile, service_name):
        self.logfile = logfile
        self.service_name = service_name
        SystemBusSysd.get_sys_bus().add_signal_receiver(
            handler_function=lambda message: print("received signal:", message),
            dbus_interface='org.freedesktop.systemd1.Manager'
        )

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
