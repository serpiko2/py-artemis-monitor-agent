from _agent.manager.DbusManager import get_sysd_manager, get_sys_bus
from _agent.scheduler.Scheduler import Job


def _restart_unit(loop, service_name, mode):
    get_sysd_manager(bus=get_sys_bus()).RestartUnit(service_name, mode,
                                                    reply_handler=lambda job: print(job),
                                                    error_handler=lambda e: print(e))
    return loop


class RestartServiceJob(Job):

    def __init__(self, service_name: str, mode: str = 'replace', delay: int = 0, loop: bool = False):
        super().__init__(_restart_unit, delay, loop)
        self._add_args(service_name, mode)

    def check_status(self, context):
        load_state = context["LoadState"]
        active_state = context["ActiveState"]
        exec_start = context["ExecStart"]
        status_code = exec_start[0][9]
        print(f"service:, load_state:{load_state}, "
              f"active_state:{active_state}, status_code:{status_code}")
        if load_state == 'loaded' and active_state == 'inactive':
            if status_code == 143:
                self.schedule()
