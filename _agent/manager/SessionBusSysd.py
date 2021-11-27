import dbus


def get_dbus_session_bus() -> dbus.SessionBus:
    """ Return a connection to the system bus.
    :returns:
        `system_bus`:`the system bus connection`
    """
    return dbus.SessionBus()
