from _agent.manager import Sysd
from _agent.scripts.CheckRestartProperties import CheckRestartProperties


def check(load_state, active_state, exec_start):
    status_code = exec_start[0][9]
    print(f"service:, load_state:{load_state}, "
          f"active_state:{active_state}, status_code:{status_code}")
    if load_state == 'loaded' and active_state == 'inactive':
        if status_code != 143:
            raise Exception


def restart_unit(properties: CheckRestartProperties, service_name, mode='replace'):
    check(properties.load_state, properties.active_state, properties.exec_start)
    return Sysd.get_sysd_manager().RestartUnit(service_name, mode)

