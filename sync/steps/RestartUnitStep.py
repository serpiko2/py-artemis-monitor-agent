from core.manager import SystemBusSysd
from sync.steps.CheckRestartProperties import CheckRestartProperties


class UserStop(Exception):
    """"""


class RestartUnitStep:

    @staticmethod
    def check_user_interruption(properties: CheckRestartProperties):
        exec_start = properties.exec_start
        load_state = properties.load_state
        active_state = properties.active_state
        status_code = exec_start[0][9]
        print(f"load_state:{load_state}, "
              f"active_state:{active_state}, status_code:{status_code}")
        if load_state == 'loaded' and active_state == 'inactive':
            if status_code == 143:
                raise UserStop

    @staticmethod
    def restart_unit_blocking(service_name, mode='replace', properties: CheckRestartProperties = None):
        if properties:
            RestartUnitStep.check_user_interruption(properties)
        return SystemBusSysd.get_sysd_manager().RestartUnit(service_name, mode)

    @staticmethod
    def restart_unit_non_blocking(service_name,
                                  mode='replace',
                                  properties: CheckRestartProperties = None,
                                  callback: callable = lambda job: print(f"restart job scheduled: {job}"),
                                  fallback: callable = lambda error: print(f"restart job error: {error} ")):
        if properties:
            RestartUnitStep.check_user_interruption(properties)
        SystemBusSysd.get_sysd_manager().RestartUnit(service_name, mode,
                                                     reply_handler=callback,
                                                     error_handler=fallback)
