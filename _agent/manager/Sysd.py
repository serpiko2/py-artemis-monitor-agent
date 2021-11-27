import sys
import traceback

import dbus
from dbus import Interface
from dbus.proxies import ProxyObject

from _agent.manager import _DbusManager

ISYSD_MANAGER_STRING = 'org.freedesktop.systemd1.Manager'
ISYSD_PROPERTIES_STRING = 'org.freedesktop.DBus.Properties'


def get_sysd_manager() -> Interface:
    return get_sysd_interface(ISYSD_MANAGER_STRING)


def get_sysd_interface(sysd_interface: str) -> Interface:
    try:
        return dbus.Interface(_DbusManager.get_sysd_proxy(),
                              dbus_interface=sysd_interface)
    except dbus.DBusException:
        traceback.print_exc()
        sys.exit(1)


def get_interface(item, interface) -> dbus.Interface:
    return Interface(item, dbus_interface=interface)


def get_properties_interface(item) -> dbus.Interface:
    return get_interface(item, ISYSD_PROPERTIES_STRING)


def get_proxy_from_object_path(object_path) -> ProxyObject:
    return _DbusManager.get_sysd_object(object_path)


def connect_to_signal(signal, callback, interface=None, connect_to=get_sysd_manager(), **parameters):
    """Arrange for a function to be called when the given signal is
    emitted.

    The parameters and keyword arguments are the same as for
    `dbus.proxies.ProxyObject.connect_to_signal`, except that if
    `dbus_interface` is None (the default), the D-Bus interface that
    was passed to the `Interface` constructor is used.
    """
    connect_to.connect_to_signal(signal, callback, dbus_interface=interface, **parameters)
