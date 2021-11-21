import dbus

from .event import subscribe
from .EventsType import Events


def print_response(data, event):
    print(f"data={data} for event={event}")


def handle_load_state_read(data: dbus.String, fun):
    fun(data, "LoadState")


def handle_active_state_read(data: dbus.String, fun):
    fun(data, "ActiveState")


def handle_exec_start_info_read(data: dbus.Array, fun):
    fun(data, "ExecStart")


def setup_dbus_monitor_events(load_state_fun,
                              active_state_fun,
                              exec_start_fun):
    __subscribe_this__(load_state_fun, active_state_fun, exec_start_fun)


def setup_dbus_monitor_events_default():
    __subscribe_this__default__()


def __subscribe_this__(load_state_fun,
                       active_state_fun,
                       exec_start_fun):
    subscribe(Events.LoadStateRead, handle_load_state_read, load_state_fun)
    subscribe(Events.ActiveStateRead, handle_active_state_read, active_state_fun)
    subscribe(Events.ExecStartInfoRead, handle_exec_start_info_read, exec_start_fun)


def __subscribe_this__default__():
    subscribe(Events.LoadStateRead, handle_load_state_read, print_response)
    subscribe(Events.ActiveStateRead, handle_active_state_read, print_response)
    subscribe(Events.ExecStartInfoRead, handle_exec_start_info_read, print_response)
