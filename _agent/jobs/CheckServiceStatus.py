from _agent.manager import Sysd
from _agent.jobs.scheduler import Job


def entrypoint(loop: bool, callback: callable, fallback: callable, items):
    """entry_point placeholder.
    """
    Sysd.get_manager().GetUnit(
        items,
        reply_handler=callback,
        error_handler=fallback
    )
    # return false to not loop
    return loop


class CheckServiceStatusJob(Job):

    def __init__(self,
                 service_name: str,
                 delay: int = 0,
                 loop=False):
        super().__init__(entrypoint, delay, loop)
        self._add_args(service_name)
        self.success = None
        self.failed = None

    def callback(self, reply):

        print(f"{reply}")
        self.success = True
        pass

    def fallback(self, error):
        print(f"{error}")
        self.failed = True
        pass

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

    def _schedule_retrieves(self, service_properties):
        Scheduler.schedule_function(self._retrieve_status, delay=0,
                                    args=(service_properties,
                                          'org.freedesktop.systemd1.Unit', 'ActiveState',
                                          EventsType.ActiveStateRead))
        Scheduler.schedule_function(self._retrieve_status, delay=0,
                                    args=(service_properties,
                                          'org.freedesktop.systemd1.Unit', 'LoadState',
                                          EventsType.LoadStateRead))
        Scheduler.schedule_function(self._retrieve_status, delay=0,
                                    args=(service_properties,
                                          'org.freedesktop.systemd1.Service', 'ExecStart',
                                          EventsType.ExecStartInfoRead))

    def _handle_update_status(self, publisher, data, update):
        update(data)
        if self._are_checks_done():
            publisher(EventsType.ReadsDone,
                                   {"LoadState": self.load_state,
                                    "ActiveState": self.active_state,
                                    "ExecStart": self.exec_start})


    def _retrieve_status(self, service_properties, interface, name, event: EventsType):
        service_properties.Get(
            interface, name,
            reply_handler=lambda data: self.publisher.publish(event, data),
            error_handler=self.handle_raise_error
        )
        return False

    def check_status(self, context):
        print("check status")
        load_state = context["LoadState"]
        active_state = context["ActiveState"]
        exec_start = context["ExecStart"]
        status_code = exec_start[0][9]
        print(f"service:, load_state:{load_state}, "
              f"active_state:{active_state}, status_code:{status_code}")
        if load_state == 'loaded' and active_state == 'inactive':
            if status_code == 143:
                self.schedule()
