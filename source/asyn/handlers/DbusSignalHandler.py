import logging

from source.asyn.jobs.ServiceJob import ServiceJob
from source.asyn.processors.DbusSignalProcessor import DbusSignalProcessor
from source.config.MonitorConfig import MonitorConfig
from source.core.manager import SystemBusSysd
from source.core.manager.SystemdNames import SystemdNames
from source.core.pubsub.EventsType import EventsType


class DbusSignalHandler(DbusSignalProcessor):
    logger = logging.getLogger(__name__)

    def __init__(self):
        super().__init__()
        ServiceJob.get_service_object_path(MonitorConfig.service_name,
                                           reply_cb=self._setup_signal_receiver,
                                           error_cb=lambda error: self._logger.error(f"{error}"))

    @classmethod
    def _setup_signal_receiver(cls, object_path):
        SystemBusSysd.get_sys_bus().add_signal_receiver(
            handler_function=lambda *args: cls._filter_unit_signal(*args),
            dbus_interface=SystemdNames.Interfaces.ISYSD_PROPERTIES_STRING,
            path=object_path  # todo check if i can filter the sender interface from here
        )

    @classmethod
    def _filter_unit_signal(cls, *args):
        interface = args[0]
        message = args[1]
        if interface == 'org.freedesktop.systemd1.Unit':
            sub_state = message['SubState']
            active_state = message['ActiveState']
            cls.logger.debug(f"received signal, "
                             f"sub_state=[{sub_state}], "
                             f"active_state=[{active_state}]")
            cls.publisher.publish(EventsType.ProcessLogStop, "Got Service signal, stopping any running process")
            if sub_state == 'running' and active_state == 'active':
                cls.logger.debug("Service was started")
                ServiceJob.get_service_object_path(MonitorConfig.service_name)
            elif sub_state == 'dead' and active_state == 'inactive':
                cls.logger.debug("Service was stopped")
                ServiceJob.get_service_object_path(MonitorConfig.service_name)
