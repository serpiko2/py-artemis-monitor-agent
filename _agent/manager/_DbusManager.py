import dbus
from dbus.proxies import ProxyObject


def get_sysd_proxy() -> ProxyObject:
    return get_dbus_sys_bus().get_object('org.freedesktop.systemd1', '/org/freedesktop/systemd1')


def get_dbus_sys_bus() -> dbus.SystemBus:
    """ Return a connection to the system bus.
    :returns:
        `system_bus`:`the system bus connection`
    """
    return dbus.SystemBus()


def get_dbus_session_bus() -> dbus.SessionBus:
    """ Return a connection to the system bus.
    :returns:
        `system_bus`:`the system bus connection`
    """
    return dbus.SessionBus()


def get_sysd_object(bus, item) -> ProxyObject:
    return bus().get_object('org.freedesktop.systemd1', item)
