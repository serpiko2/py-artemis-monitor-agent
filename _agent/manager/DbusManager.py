import dbus
import traceback
import sys


def get_sys_bus() -> dbus.SystemBus:
    """ Return a connection to the system bus.
    :returns:
        `system_bus`:`the system bus connection`
    """
    return dbus.SystemBus()


def get_sysd_manager(bus: dbus.SystemBus):
    """ Return the systemd proxy object and the manager interface.
    :param:
        `bus`:`the system bus connection`
    :returns:
        `sysd_manager_interface`:`the systemd manager interface`
    """
    try:
        sysd1 = get_sysd_object('/org/freedesktop/systemd1', bus)
        return dbus.Interface(sysd1, dbus_interface='org.freedesktop.systemd1.Manager')
    except dbus.DBusException:
        traceback.print_exc()
        sys.exit(1)


def get_sysd_interface(bus: dbus.SystemBus,
                       sysd_interface=str):
    """Setup and return the systemd proxy object and the manager interface.
    :param:
        `bus`:`the system bus connection`
        `sysd_interface`:`the systemd interface class`
    :returns:
        `sysd_interface`:`the systemd service interface`
    """
    try:
        sysd1 = get_sysd_object('/org/freedesktop/systemd1', bus)
        return dbus.Interface(sysd1, dbus_interface=sysd_interface)
    except dbus.DBusException:
        traceback.print_exc()
        sys.exit(1)


def get_sysd_object(item, bus: dbus.SystemBus):
    """Setup the systemd proxy object and the manager interface.
    :param:
        `bus`:`the system bus connection`
        `sysd_interface`:`the systemd interface class`
    :returns:
        `sysd_interface`:`the systemd service interface`
    """
    return bus.get_object('org.freedesktop.systemd1', item)
