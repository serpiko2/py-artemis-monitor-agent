from _agent.manager import SystemBusSysd


def get_service(service_name: str):
    return SystemBusSysd.get_sysd_manager().GetUnit(
        service_name
    )
