from _agent.events.Events import Subscriber
from _agent.events.UnitCheck.EventsType import EventsType
from _agent.events.UnitCheck.ServiceStatusSource import ServiceStatusSource
from _agent.manager.DbusManager import get_sys_bus, get_sysd_manager
from _agent.scheduler.Scheduler import Job


def _find_service_unit(loop, service_name: str, reply_cb, error_cb):
    """Find the service unit by it's name.
        :param:
            `name`:`the formatted service name as {name}.service`
            `loop`:`true or false to make it loop`
        :returns:
            `service_object_path`:`the service object path reference`
    """
    get_sysd_manager(bus=get_sys_bus()).GetUnit(
        service_name,
        reply_handler=reply_cb,
        error_handler=error_cb
    )
    # return false to not loop
    return loop


class ServiceStatusJob(Job):

    def __init__(self, service_name: str, source: ServiceStatusSource, delay: int = 0, loop=False):
        super().__init__(_find_service_unit, delay, loop)
        self._add_args(service_name, source, source.handle_get_unit_callback, source.handle_raise_error)
        self.active_state = None
        self.load_state = None
        self.exec_start = None

    def _set_active_state(self, data):
        self.active_state = data

    def _set_load_state(self, data):
        self.load_state = data

    def _set_exec_start(self, data):
        self.exec_start = data

    def _are_checks_done(self):
        if self.exec_start and self.load_state and self.active_state:
            return True
        return False

    def _setup_sink(self, publisher, name='PropertiesListener'):
        listener = Subscriber(name)
        listener.subscribe(EventsType.ActiveStateRead,
                           publisher,
                           callback=lambda message:
                           self._handle_update_status(message, self._set_active_state))
        listener.subscribe(EventsType.LoadStateRead,
                           publisher,
                           callback=lambda message:
                           self._handle_update_status(message, self._set_load_state))
        listener.subscribe(EventsType.ExecStartInfoRead,
                           publisher,
                           callback=lambda message:
                           self._handle_update_status(message, self._set_exec_start))
        return listener

    def _handle_update_status(self, data, update):
        update(data)
        if self._are_checks_done():
            print("checks done")
            self.publisher.publish(EventsType.ReadsDone,
                                   {"LoadState": self.load_state,
                                    "ActiveState": self.active_state,
                                    "ExecStart": self.exec_start})
