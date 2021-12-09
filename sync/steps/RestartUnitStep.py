from core.manager import SystemBusSysd
from sync.steps.CheckRestartProperties import CheckRestartProperties


class UserStop(Exception):
    """"""


class RestartUnitStep:

    @staticmethod
    def check(load_state, active_state, exec_start):
        status_code = exec_start[0][9]
        print(f"service:, load_state:{load_state}, "
              f"active_state:{active_state}, status_code:{status_code}")
        if load_state == 'loaded' and active_state == 'inactive':
            if status_code == 143:
                raise UserStop

    @staticmethod
    def restart_unit_async(service_name, mode='replace', properties: CheckRestartProperties = None):
        if properties:
            RestartUnitStep.check(properties.load_state, properties.active_state, properties.exec_start)
        SystemBusSysd.get_sysd_manager().RestartUnit(service_name, mode,
                                                     reply_handler=lambda job: print(f"restart job scheduled: {job}"),
                                                     error_handler=lambda error: print(f"restart job error: {error} "))
