import sys
import traceback
from gi.repository import GLib
import dbus
import dbus.mainloop.glib
from dbus import Interface

from events import properties_listener
from events import event
from events import EventsType


load_state = None
load_state_trigger = False
active_state = None
active_state_trigger = False
status_code = None
status_code_trigger = False


# ################################
# START Callbacks for asynchronous calls
# ################################
def handle_load_state_monitor_event(*items):
    print(f"handle monitor event {items}")
    global load_state
    global load_state_trigger
    load_state = items[0]
    load_state_trigger = True
    is_monitoring_done()


def handle_active_state_monitor_event(*items):
    print(f"handle monitor event {items}")
    global active_state
    global active_state_trigger
    active_state = items[0]
    active_state_trigger = True
    is_monitoring_done()


def handle_exec_start_monitor_event(*items):
    print(f"handle monitor event {items}")
    global status_code
    global status_code_trigger
    status_code = items[0][0][9]
    status_code_trigger = True
    is_monitoring_done()


def is_monitoring_done():
    if status_code_trigger and active_state_trigger and load_state_trigger:
        print("monitoring done")
        handle_systemd_read()


def handle_get_unit_callback(unit):
    """handle the get unit callback for monitoring.
        :param:
            `unit`:`the unit object path`
    """
    global sysd_manager
    global system_bus
    if unit:
        unit_object = system_bus.get_object('org.freedesktop.systemd1', unit)
        service_properties = Interface(unit_object, dbus_interface='org.freedesktop.DBus.Properties')
        # let's the event handler take care of reacting the the complete read
        service_properties.Get('org.freedesktop.systemd1.Unit', 'LoadState',
                               reply_handler=lambda data: event.post(EventsType.Events.LoadStateRead, data),
                               error_handler=handle_raise_error)
        service_properties.Get('org.freedesktop.systemd1.Unit', 'ActiveState',
                               reply_handler=lambda data: event.post(EventsType.Events.ActiveStateRead, data),
                               error_handler=handle_raise_error)
        service_properties.Get('org.freedesktop.systemd1.Service', 'ExecStart',
                               reply_handler=lambda data: event.post(EventsType.Events.ExecStartInfoRead, data),
                               error_handler=handle_raise_error)


def handle_raise_error(e):
    print(f"async client status: ExceptionRaise {e}")
    # if an error happens on read i don't need to quit
    # loop.quit()

# ################################
# END Callbacks for asynchronous calls
# ################################


def handle_systemd_read():
    print(f"{load_state}, {active_state}, {status_code}")
    if load_state == 'loaded' and active_state == 'inactive' and status_code == 143:
        sysd_manager.RestartUnit("artemis.service",
                                 "replace",
                                 reply_handler=lambda a: print(a),
                                 error_handler=handle_raise_error)


def setup_sysd_bus_manager_interface(bus):
    """Setup the systemd proxy object and the manager interface.
        :param:
            `bus`:`the system bus reference from dbus`
        :returns:
            `sysd_manager_interface`:`the systemd service manager interface`
    """
    try:
        sysd1 = bus.get_object('org.freedesktop.systemd1',
                               '/org/freedesktop/systemd1')
        return dbus.Interface(sysd1,
                              dbus_interface='org.freedesktop.systemd1.Manager')
    except dbus.DBusException:
        traceback.print_exc()
        sys.exit(1)


def find_service_unit(name):
    """Find the service unit by it's name.
        :param:
            `name`:`the formatted service name as {name}.service`
        :returns:
            `service_object_path`:`the service object path reference`
    """
    global sysd_manager
    sysd_manager.GetUnit(name,
                         reply_handler=handle_get_unit_callback,
                         error_handler=handle_raise_error)
    # return false to not loop
    return False


if __name__ == '__main__':
    # Set glib main loop
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    # Get the system bus
    system_bus = dbus.SystemBus()
    sysd_manager = setup_sysd_bus_manager_interface(system_bus)
    # setup the property listener
    properties_listener.setup_dbus_monitor_events(load_state_fun=handle_load_state_monitor_event,
                                                  active_state_fun=handle_active_state_monitor_event,
                                                  exec_start_fun=handle_exec_start_monitor_event)
    # properties_listener.setup_dbus_monitor_events()
    GLib.timeout_add(1, find_service_unit, "artemis.service")
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
    service_unit = service_name if service_name.endswith('.service') else sysd_manager.GetUnit(
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
