import sys
from gi.repository import GLib
from dbus import Interface

from agent.events.Events import Publisher
from agent.events.UnitCheck.EventsType import EventsType
from agent.events.UnitCheck.PropertiesListener import PropertiesListener
from agent.manager.DbusManager import get_sys_bus, get_sysd_manager, get_sysd_object


class UnitNotFoundException(Exception):
    def __init__(self, obj):
        self.obj = obj


class ServiceStatusProcessor:

    def _entrypoint(self, delay, loop):
        GLib.timeout_add(delay, self._find_service_unit, "artemis.service", loop)

    def _find_service_unit(self, service_name, loop):
        """Find the service unit by it's name.
            :param:
                `name`:`the formatted service name as {name}.service`
                `loop`:`true or false to make it loop`
            :returns:
                `service_object_path`:`the service object path reference`
        """
        get_sysd_manager(bus=get_sys_bus()).GetUnit(
            service_name,
            reply_handler=self.handle_get_unit_callback,
            error_handler=self.handle_raise_error
        )
        # return false to not loop
        return loop

    def _setup_publisher(self):
        properties_publisher = Publisher([EventsType.LoadStateRead,
                                          EventsType.ActiveStateRead,
                                          EventsType.ExecStartInfoRead])
        self.properties_publisher = properties_publisher

    def _setup_listener(self, publisher, name='PropertiesListener'):
        properties_listener = PropertiesListener(name)
        properties_listener.subscribe(EventsType.LoadStateRead,
                                      publisher,
                                      callback=self.update_monitoring_status)
        properties_listener.subscribe(EventsType.ActiveStateRead,
                                       publisher,
                                       callback=self.update_monitoring_status)
        properties_listener.subscribe(EventsType.ExecStartInfoRead,
                                       publisher,
                                       callback=self.update_monitoring_status)
        self.properties_listener = properties_listener

    def __init__(self, ):
        self._setup_publisher()
        self._setup_listener(self.properties_publisher)


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
            service_properties.Get(
                'org.freedesktop.systemd1.Unit', 'LoadState',
                reply_handler=lambda data: self.properties_publisher.publish(EventsType.LoadStateRead, data),
                error_handler=self.handle_raise_error
            )
            service_properties.Get(
                'org.freedesktop.systemd1.Unit', 'ActiveState',
                reply_handler=lambda data: self.properties_publisher.publish(EventsType.ActiveStateRead, data),
                error_handler=self.handle_raise_error
            )
            service_properties.Get(
                'org.freedesktop.systemd1.Service', 'ExecStart',
                reply_handler=lambda data: self.properties_publisher.publish(EventsType.ExecStartInfoRead, data),
                error_handler=self.handle_raise_error
            )
        else:
            raise UnitNotFoundException(self.__hash__())


    def handle_raise_error(self, e):
        print(f"async client {self} status: ExceptionRaise {e}")
        # if an error happens on read i don't need to quit
        # loop.quit()

    """
    # END Callbacks for asynchronous calls
    """

    """
        WIP
    """
    def update_monitoring_status(self, data):
        print("monitoring done", data)
        #handle_systemd_read()

    def handle_systemd_read(self):
        get_sysd_manager(bus=get_sys_bus()).RestartUnit("artemis.service",
                                 "replace",
                                 reply_handler=lambda a: print(a),
                                 error_handler=lambda a: print(a))
    """
        WIP
    """




    def wip(self):
        service_name = str(sys.argv[1]) if str(sys.argv[1]).endswith('.service') else '{0}.service'.format(
            str(sys.argv[1])) if len(sys.argv) > 2 else "artemis"
        print(f"service name: {service_name}")
        service_unit = service_name if service_name.endswith('.service') else get_sysd_object.GetUnit(
            '{0}.service'.format(service_name))
        print(f"service unit: {service_unit}")
        service_load_state = ""
        service_active_state = "active"
        if service_load_state == 'loaded' and service_active_state == 'active':
            print('service_running = True')
        else:
            print('SERVICE NOT RUN')
        # print(service_properties.Get('org.freedesktop.systemd1.Service', 'ExecStart'))
        # sysd_manager.RestartUnit("artemis.service",
        #                        "replace",
        #                        reply_handler=lambda a: print(a),
        #                        error_handler=handle_raise_error)

