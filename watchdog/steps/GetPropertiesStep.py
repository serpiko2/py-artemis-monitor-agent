import dbus
from dbus import Interface

from core.manager import SystemBusSysd
from watchdog.steps.CheckRestartProperties import CheckRestartProperties


class Interfaces:
    Unit = 'org.freedesktop.systemd1.Unit'
    Service = 'org.freedesktop.systemd1.Service'


class Properties:
    ActiveState = 'ActiveState'
    LoadState = 'LoadState'
    ExecStart = 'ExecStart'


class GetPropertiesStep:

    @staticmethod
    def get_properties_for_restart(service_properties: Interface):
        return CheckRestartProperties(service_properties.Get(
            Interfaces.Unit, Properties.ActiveState
        ), service_properties.Get(
            Interfaces.Unit, Properties.LoadState
        ), service_properties.Get(
            Interfaces.Service, Properties.ExecStart
        ))

    @staticmethod
    def get_service_properties(unit: dbus.ObjectPath):
        unit_object = SystemBusSysd.get_proxy_from_object_path(unit)
        service_properties = SystemBusSysd.get_properties_interface(unit_object)
        return service_properties
