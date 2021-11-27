import dbus
from dbus import Interface

from _agent.manager import Sysd
from _agent.procedures.steps.Step import Step


class Interfaces:
    Unit = 'org.freedesktop.systemd1.Unit'
    Service = 'org.freedesktop.systemd1.Service'


class Properties:
    ActiveState = 'ActiveState'
    LoadState = 'LoadState'
    ExecStart = 'ExecStart'


class GetPropertiesStep(Step):

    def __init__(self):
        super().__init__()

    def apply(self, service_properties: Interface):
        return {'load_state': service_properties.Get(
            Interfaces.Unit, Properties.ActiveState
        ), 'active_state': service_properties.Get(
            Interfaces.Unit, Properties.LoadState
        ), 'exe_start': service_properties.Get(
            Interfaces.Service, Properties.ExecStart
        )}

    def before(self, unit: dbus.ObjectPath):
        unit_object = Sysd.get_proxy_from_object_path(unit)
        service_properties = Sysd.get_properties_interface(unit_object)
        return service_properties
