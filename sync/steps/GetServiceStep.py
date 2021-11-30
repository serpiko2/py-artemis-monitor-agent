from core.manager import SystemBusSysd


class GetServiceStep:

    @staticmethod
    def get_service(service_name: str):
        return SystemBusSysd.get_sysd_manager().GetUnit(
            service_name
        )
