import dbus
from dbus.proxies import ProxyObject


def get_sysd_proxy() -> ProxyObject:
    return get_sys_bus().get_object('org.freedesktop.systemd1', '/org/freedesktop/systemd1')


def get_sys_bus() -> dbus.SessionBus:
    """ Return a connection to the system bus.
    :returns:
        `system_bus`:`the system bus connection`
    """
    return dbus.SessionBus()


def get_sysd_object(item) -> ProxyObject:
    return get_sys_bus().get_object('org.freedesktop.systemd1', item)
