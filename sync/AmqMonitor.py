from datetime import datetime

import dbus

from core.Logger import Logger
from core.manager import SystemBusSysd
from core.manager.SystemdNames import SystemdNames
from core.scheduler.Scheduler import Scheduler
from sync.MonitorLogFileProcess import MonitorLogFileProcess
from sync.steps.GetPropertiesStep import GetPropertiesStep
from sync.steps.GetServiceStep import GetServiceStep
from sync.steps.RestartUnitStep import RestartUnitStep


class AmqMonitor:

    def __init__(self, log_path, service_name):
        self.logger = Logger.get_logger(self.__class__.__name__)
        self.service_name = service_name
        self.file_handler = MonitorLogFileProcess(log_path, service_name)
        try:
            self.unit = GetServiceStep.get_service(self.service_name)
            self._setup_signal_sink()
        except dbus.DBusException as e:
            self.logger.exception("unit not found, ", e)
            Scheduler.kill_loop(1)

    def _setup_signal_sink(self):
        SystemBusSysd.get_sys_bus().add_signal_receiver(
            handler_function=self._filter_unit_signal,
            dbus_interface=SystemdNames.Interfaces.ISYSD_PROPERTIES_STRING,
            path=self.unit  # todo check if i can filter the sender interface from here
        )

    def _filter_unit_signal(self, *args):
        interface = args[0]
        message = args[1]
        ts_event_received = datetime.now()
        if interface == 'org.freedesktop.systemd1.Unit':
            sub_state = message['SubState']
            active_state = message['ActiveState']
            self.logger.info(f"{ts_event_received} SubState: {message['SubState']}")
            self.logger.info(f"{ts_event_received} ActiveState: {message['ActiveState']}")
            if active_state == "active" and sub_state == "running":
                self.file_handler.stop()
            if active_state == "inactive" and sub_state == "dead":
                self.file_handler.stop()
                self.file_handler.start()

    def blocking_restart_on_demand(self):
        unit = GetServiceStep.get_service(self.service_name)
        service_properties = GetPropertiesStep.get_service_properties(unit)
        properties = GetPropertiesStep.get_properties_for_restart(service_properties)
        restart_job_result = RestartUnitStep.restart_unit_blocking(properties, self.service_name)
        return restart_job_result
