import dbus


def get_dbus_session_bus() -> dbus.SessionBus:
    """ Return a connection to the system bus.
    :returns:
        `system_bus`:`the system bus connection`
    """
    return dbus.SessionBus()


def get_sysd_proxy_object():
    return get_dbus_session_bus().get_object('org.freedesktop.systemd1', '/org/freedesktop/systemd1')
