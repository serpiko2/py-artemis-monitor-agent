from _agent.manager import Sysd
from _agent.procedures.steps.Step import Step


class RestartUnitStep(Step):

    def __init__(self, service_name, mode = 'replace'):
        self.service_name = service_name
        self.mode = mode

    def apply(self):
        return Sysd.get_sysd_manager().RestartUnit(self.service_name, self.mode)

    def before(self, load_state, active_state, exec_start):
        status_code = exec_start[0][9]
        print(f"service:, load_state:{load_state}, "
              f"active_state:{active_state}, status_code:{status_code}")
        if load_state == 'loaded' and active_state == 'inactive':
            if status_code != 143:
                raise Exception
