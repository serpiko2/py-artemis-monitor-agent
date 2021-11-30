from datetime import datetime

import dbus

from core.manager import SystemBusSysd
from core.manager.SystemdNames import SystemdNames
from core.scheduler import Scheduler
from sync.steps.MmapReadFileStep import FileHandler
from sync.steps.GetPropertiesStep import GetPropertiesStep
from sync.steps.GetServiceStep import GetServiceStep
from sync.steps.RestartUnitStep import RestartUnitStep


class AmqSyncMonitor:

    def __init__(self, logfile, service_name):
        self.logfile = logfile
        self.service_name = service_name
        self.file_handler = FileHandler()
        try:
            self.unit = GetServiceStep.get_service(self.service_name)
        except dbus.DBusException as e:
            print("unit not found, ", e)
            Scheduler.kill_loop(1)
        self._setup_signal_sink()

    def _setup_signal_sink(self):
        print(f"unit object: {self.unit}")
        SystemBusSysd.get_sys_bus().add_signal_receiver(
            handler_function=lambda *signal:
            self._filter_unit_signal(*signal),
            dbus_interface=SystemdNames.Interfaces.ISYSD_PROPERTIES_STRING,
            path=self.unit
        )

    def _filter_unit_signal(self, *args):
        print("signal received")
        interface = args[0]
        message = args[1]
        ts_event_received = datetime.now()
        if interface == 'org.freedesktop.systemd1.Unit':
            sub_state = message['SubState']
            active_state = message['ActiveState']
            print(f"{ts_event_received} SubState: {message['SubState']}")
            print(f"{ts_event_received} ActiveState: {message['ActiveState']}")
            if active_state == "inactive" and sub_state == "dead":
                self.file_handler.force_exit()
                self.check_from_logs()

    def check_from_logs(self):
        self.file_handler.seek_to_end_and_tail(filename=self.logfile)

    def restart(self):
        unit = GetServiceStep.get_service(self.service_name)
        service_properties = GetPropertiesStep.get_service_properties(unit)
        properties = GetPropertiesStep.get_properties_for_restart(service_properties)
        restart_job = RestartUnitStep.restart_unit(properties, self.service_name)
        # reset restart counter
        return restart_job
