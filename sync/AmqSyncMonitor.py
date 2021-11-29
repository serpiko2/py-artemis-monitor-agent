from core.manager import SystemBusSysd
from sync.steps.GetPropertiesStep import GetPropertiesStep
from sync.steps.GetServiceStep import GetServiceStep
from sync.steps.RestartUnitStep import RestartUnitStep


class AmqSyncMonitor:

    stop_sink = SystemBusSysd.get_sysd_manager().connect_to_signal("JobRemoved", lambda m: print(m))

    @staticmethod
    def check_and_restart(service_name: str):
        unit = GetServiceStep.get_service(service_name)
        service_properties = GetPropertiesStep.get_service_properties(unit)
        properties = GetPropertiesStep.get_properties_for_restart(service_properties)
        restart_job = RestartUnitStep.restart_unit(properties, service_name)
        return restart_job
