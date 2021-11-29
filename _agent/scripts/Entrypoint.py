from _agent.scripts import GetServiceStep, GetPropertiesStep, RestartUnitStep


def check_and_restart(service_name: str):
    unit = GetServiceStep.get_service(service_name)
    service_properties = GetPropertiesStep.get_service_properties(unit)
    properties = GetPropertiesStep.get_properties_for_restart(service_properties)
    restart_job = RestartUnitStep.restart_unit(properties, service_name)
    return restart_job
