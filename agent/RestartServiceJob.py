from agent.manager.DbusManager import get_sysd_manager, get_sys_bus
from agent.scheduler import Scheduler
from agent.scheduler.Scheduler import Job


class RestartServiceJob(Job):

    def __init__(self, service_name, mode='replace', delay: int=0, loop=False):
        super().__init__(self._restart_unit, delay)
        self.loop = loop
        self.service_name = service_name
        self.mode = mode

    def schedule(self):
        Scheduler.schedule_function(self.func)

    def check_status(self, context):
        load_state = context["LoadState"]
        active_state = context["ActiveState"]
        exec_start = context["ExecStart"]
        status_code = exec_start[0][9]
        print(f"service:{self.service_name}, load_state:{load_state}, "
              f"active_state:{active_state}, status_code:{status_code}")
        if load_state == 'loaded' and active_state == 'inactive':
            if status_code == 143:
                Scheduler.schedule_function(self.func)


    def _restart_unit(self):
        get_sysd_manager(bus=get_sys_bus()).RestartUnit(self.service_name, self.mode,
                                                        reply_handler=lambda job: print(job),
                                                        error_handler=lambda e: print(e))
        return self.loop
