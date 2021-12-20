from datetime import datetime

import dbus

from core.Logger import Logger
from core.manager import SystemBusSysd
from core.manager.SystemdNames import SystemdNames
from core.scheduler.Scheduler import Scheduler
from sync.MonitorLogFileProcess import MonitorLogFileProcess
from sync.steps.GetPropertiesStep import GetPropertiesStep
from sync.steps.GetServiceStep import GetServiceStep
from sync.steps.RestartUnitStep import RestartUnitStep, UserStop


class AmqMonitor:

    def __init__(self, log_path, service_name):
        self.logger = Logger.get_logger(self.__class__.__name__)
        self.service_name = service_name
        self.file_handler = MonitorLogFileProcess(log_path, service_name)
        self.unit_object_path = GetServiceStep.get_service(self.service_name)
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
        self.logger.info(f"interface={interface} , message={message}")
        if interface == 'org.freedesktop.systemd1.Unit':
            sub_state = message['SubState']
            active_state = message['ActiveState']
            self.logger.info(f"SubState: {message['SubState']}")
            self.logger.info(f"ActiveState: {message['ActiveState']}")
            if active_state == "active" and sub_state == "running":
                self.file_handler.stop()
            if active_state == "inactive" and sub_state == "dead":
                self.file_handler.stop()
                service_properties = GetPropertiesStep.get_service_properties(self.unit_object_path)
                properties = GetPropertiesStep.get_properties_for_restart(service_properties)
                try:
                    RestartUnitStep.check_user_interruption(properties)
                    self.file_handler.start()
                except UserStop:
                    self.logger.error(f"Service {self.service_name} stopped by user")

    def blocking_restart_on_demand(self):
        unit = GetServiceStep.get_service(self.service_name)
        service_properties = GetPropertiesStep.get_service_properties(unit)
        properties = GetPropertiesStep.get_properties_for_restart(service_properties)
        restart_job_result = RestartUnitStep.restart_unit_blocking(properties, self.service_name)
        return restart_job_result
