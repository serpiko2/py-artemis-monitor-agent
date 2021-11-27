import sys
import traceback

import dbus
from dbus import Interface
from dbus.proxies import ProxyObject

ISYSD_MANAGER_STRING = 'org.freedesktop.systemd1.Manager'
ISYSD_PROPERTIES_STRING = 'org.freedesktop.DBus.Properties'


def get_sysd_proxy() -> ProxyObject:
    return get_sys_bus().get_object('org.freedesktop.systemd1', '/org/freedesktop/systemd1')


def get_sys_bus() -> dbus.SystemBus:
    """ Return a connection to the system bus.
    :returns:
        `system_bus`:`the system bus connection`
    """
    return dbus.SystemBus()


def get_sysd_object(item) -> ProxyObject:
    return get_sys_bus().get_object('org.freedesktop.systemd1', item)


def get_sysd_manager() -> Interface:
    return get_sysd_interface(ISYSD_MANAGER_STRING)


def get_sysd_interface(sysd_interface: str) -> Interface:
    try:
        return dbus.Interface(get_sysd_proxy(),
                              dbus_interface=sysd_interface)
    except dbus.DBusException:
        traceback.print_exc()
        sys.exit(1)


def get_interface(item, interface) -> dbus.Interface:
    return Interface(item, dbus_interface=interface)


def get_properties_interface(item) -> dbus.Interface:
    return get_interface(item, ISYSD_PROPERTIES_STRING)


def get_proxy_from_object_path(object_path) -> ProxyObject:
    return get_sysd_object(object_path)
