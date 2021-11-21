import dbus
import traceback
import sys


def _setup_sysd_bus_manager_interface(bus: dbus.SystemBus):
    """Setup the systemd proxy object and the manager interface.
    :param:
        `bus`:`the system bus reference from dbus`
    :returns:
        `sysd_manager_interface`:`the systemd service manager interface`
    """
    try:
        sysd1 = bus.get_object('org.freedesktop.systemd1', '/org/freedesktop/systemd1')
        return dbus.Interface(sysd1, dbus_interface='org.freedesktop.systemd1.Manager')
    except dbus.DBusException:
        traceback.print_exc()
        sys.exit(1)

class DbusManager:
    """ Dbus manager to be used for every call to the system bus or to
        the systemd manager interface, we don't want to reserve more than one
        slot on the bus for an application
    """
    system_bus: dbus.SystemBus
    sysd_manager: dbus.Interface

    def __init__(self):
        sysbus = dbus.SystemBus()
        self.system_bus = sysbus
        self.sysd_manager = _setup_sysd_bus_manager_interface(sysbus)