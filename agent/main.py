import sys
import traceback
from gi.repository import GLib
import dbus.mainloop.glib
from dbus import Interface

from events.UnitCheck import EventsType
from manager.DbusManager import DbusManager


from events import Events

# ################################
# START Callbacks for asynchronous calls

# ################################

def is_monitoring_done(data):
    #if restart_listener.status_code_trigger and restart_listener.active_state_trigger and restart_listener.load_state_trigger:
        print("monitoring done", data)
        #handle_systemd_read()


def handle_systemd_read():
    #print(f"{restart_listener.load_state}, "
    #      f"{restart_listener.active_state}, "
    #     f"{restart_listener.status_code}")
    #if restart_listener.load_state == 'loaded' \
    #        and restart_listener.active_state == 'inactive' \
    #        and restart_listener.status_code == 143:
        dbus_manager.sysd_manager.RestartUnit("artemis.service",
                                 "replace",
                                 reply_handler=lambda a: print(a),
                                 error_handler=lambda a: print(a))


def handle_get_unit_callback(unit):
    """handle the get unit callback for monitoring.
        :param:
            `unit`:`the unit object path`
    """
    print('found service unit')
    if unit:
        unit_object = dbus_manager.system_bus.get_object('org.freedesktop.systemd1', unit)
        service_properties = Interface(unit_object, dbus_interface='org.freedesktop.DBus.Properties')
        # let's the event handler take care of reacting the the complete read
        service_properties.Get('org.freedesktop.systemd1.Unit', 'LoadState',
                               reply_handler=lambda data: properties_publisher.publish(EventsType.Events.LoadStateRead, data),
                               error_handler=handle_raise_error)
        service_properties.Get('org.freedesktop.systemd1.Unit', 'ActiveState',
                               reply_handler=lambda data: properties_publisher.publish(EventsType.Events.ActiveStateRead, data),
                               error_handler=handle_raise_error)
        service_properties.Get('org.freedesktop.systemd1.Service', 'ExecStart',
                               reply_handler=lambda data: properties_publisher.publish(EventsType.Events.ExecStartInfoRead, data),
                               error_handler=handle_raise_error)


def handle_raise_error(e):
    print(f"async client status: ExceptionRaise {e}")
    # if an error happens on read i don't need to quit
    # loop.quit()

# ################################
# END Callbacks for asynchronous calls
# ################################

def find_service_unit(name):
    """Find the service unit by it's name.
        :param:
            `name`:`the formatted service name as {name}.service`
        :returns:
            `service_object_path`:`the service object path reference`
    """
    print("finding service unit")
    dbus_manager.sysd_manager.GetUnit(name,
                         reply_handler=handle_get_unit_callback,
                         error_handler=handle_raise_error)
    # return false to not loop
    return False

if __name__ == '__main__':
    # Set glib main loop
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    dbus_manager = DbusManager()
    properties_publisher = Events.Publisher([EventsType.Events.LoadStateRead,
                                             EventsType.Events.ActiveStateRead,
                                             EventsType.Events.ExecStartInfoRead])
    properties_listener = Events.Subscriber('PropertiesListener')

    properties_publisher.subscribe(EventsType.Events.LoadStateRead,
                                   properties_listener,
                                   callback=is_monitoring_done)
    properties_publisher.subscribe(EventsType.Events.ActiveStateRead,
                                   properties_listener,
                                   callback=is_monitoring_done)
    properties_publisher.subscribe(EventsType.Events.ExecStartInfoRead,
                                   properties_listener,
                                   callback=is_monitoring_done)
    # setup the property listener
    # properties_listener.setup_dbus_monitor_events()
    GLib.timeout_add(10, find_service_unit, "artemis.service")
    loop = GLib.MainLoop()
    try:
        loop.run()
    except KeyboardInterrupt:
        traceback.print_exc()
        loop.quit()


def wip():
    service_name = str(sys.argv[1]) if str(sys.argv[1]).endswith('.service') else '{0}.service'.format(
        str(sys.argv[1])) if len(sys.argv) > 2 else "artemis"
    print(f"service name: {service_name}")
    service_unit = service_name if service_name.endswith('.service') else dbus_manager.sysd_manager.GetUnit(
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
