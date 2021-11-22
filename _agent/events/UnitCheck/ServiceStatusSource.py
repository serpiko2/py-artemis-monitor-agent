from dbus import Interface
from _agent.events.Events import Subscriber
from _agent.events.UnitCheck.EventsType import EventsType
from _agent.manager.DbusManager import get_sysd_object, get_sys_bus
from _agent.scheduler import Scheduler


class UnitNotFoundException(Exception):
    def __init__(self, obj):
        self.obj = obj


class ServiceStatusSource:

    def _retrieve_status(self, service_properties, interface, name, event: EventsType):
        service_properties.Get(
            interface, name,
            reply_handler=lambda data: self.publisher.publish(event, data),
            error_handler=self.handle_raise_error
        )
        return False

    def __init__(self, publisher):
        self.publisher = publisher

    """
    # START Callbacks for asynchronous calls
    """

    def handle_get_unit_callback(self, unit):
        """handle the get unit callback for monitoring.
            :param:
                `unit`:`the unit object path`
        """
        if unit:
            unit_object = get_sysd_object(unit, bus=get_sys_bus())
            service_properties = Interface(unit_object, dbus_interface='org.freedesktop.DBus.Properties')
            Scheduler.schedule_function(self._retrieve_status, delay=0,
                                        args=(service_properties,
                                              'org.freedesktop.systemd1.Unit', 'ActiveState',
                                              EventsType.ActiveStateRead))
            Scheduler.schedule_function(self._retrieve_status, delay=0,
                                        args=(service_properties,
                                              'org.freedesktop.systemd1.Unit', 'LoadState',
                                              EventsType.LoadStateRead))
            Scheduler.schedule_function(self._retrieve_status, delay=0,
                                        args=(service_properties,
                                              'org.freedesktop.systemd1.Service', 'ExecStart',
                                              EventsType.ExecStartInfoRead))
        else:
            raise UnitNotFoundException(self.__hash__())

    def handle_raise_error(self, e):
        print(f"async client {self} status: ExceptionRaise {e}")
        # if an error happens on read i don't need to quit
        # loop.quit()

    """
    # END Callbacks for asynchronous calls
    """
