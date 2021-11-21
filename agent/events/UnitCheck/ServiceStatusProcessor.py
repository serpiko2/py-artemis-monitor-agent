from dbus import Interface
from agent.events.Events import Subscriber
from agent.events.UnitCheck.EventsType import EventsType
from agent.manager.DbusManager import get_sysd_object, get_sys_bus
from agent.scheduler import Scheduler


class UnitNotFoundException(Exception):
    def __init__(self, obj):
        self.obj = obj


class ServiceStatusProcessor:

    def _setup_listener(self, publisher, name='PropertiesListener'):
        properties_listener = Subscriber(name)
        properties_listener.subscribe(EventsType.ActiveStateRead,
                                      publisher,
                                      callback=lambda message:
                                      self.handle_update_status(message, self._set_active_state))
        properties_listener.subscribe(EventsType.LoadStateRead,
                                      publisher,
                                      callback=lambda message:
                                        self.handle_update_status(message, self._set_load_state))
        properties_listener.subscribe(EventsType.ExecStartInfoRead,
                                       publisher,
                                       callback=lambda message:
                                        self.handle_update_status(message, self._set_exec_start))
        return properties_listener

    def _retrieve_status(self, service_properties, interface, name, event: EventsType):
        service_properties.Get(
            interface, name,
            reply_handler=lambda data: self.properties_publisher.publish(event, data),
            error_handler=self.handle_raise_error
        )
        return False

    def __init__(self, publisher):
        self.properties_publisher = publisher
        self.properties_listener = self._setup_listener(publisher)
        self.active_state = None
        self.load_state = None
        self.exec_start = None

    def _set_active_state(self, data):
        self.active_state = data

    def _set_load_state(self, data):
        self.load_state = data

    def _set_exec_start(self, data):
        self.exec_start = data

    def _are_checks_done(self):
        if self.exec_start and self.load_state and self.active_state:
            return True
        return False

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
            Scheduler.schedule_function(self._retrieve_status, 0, service_properties,
                             'org.freedesktop.systemd1.Unit', 'ActiveState',
                                        EventsType.ActiveStateRead)
            Scheduler.schedule_function(self._retrieve_status, 0, service_properties,
                             'org.freedesktop.systemd1.Unit', 'LoadState',
                             EventsType.LoadStateRead)
            Scheduler.schedule_function(self._retrieve_status, 0, service_properties,
                             'org.freedesktop.systemd1.Service', 'ExecStart',
                             EventsType.ExecStartInfoRead)
        else:
            raise UnitNotFoundException(self.__hash__())

    def handle_update_status(self, data, update):
        update(data)
        if self._are_checks_done():
            print("checks done")
            self.properties_publisher.publish(EventsType.ReadsDone,
                                              {"LoadState":self.load_state,
                                               "ActiveState":self.active_state,
                                               "ExecStart":self.exec_start})

    def handle_raise_error(self, e):
        print(f"async client {self} status: ExceptionRaise {e}")
        # if an error happens on read i don't need to quit
        # loop.quit()
    """
    # END Callbacks for asynchronous calls
    """
