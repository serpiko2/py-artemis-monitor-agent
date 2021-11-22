from _agent.events.UnitCheck.ServiceStatusProcessor import ServiceStatusProcessor
from _agent.manager.DbusManager import get_sys_bus, get_sysd_manager
from _agent.scheduler.Scheduler import Job


def _find_service_unit(loop, service_name: str, processor: ServiceStatusProcessor):
    """Find the service unit by it's name.
        :param:
            `name`:`the formatted service name as {name}.service`
            `loop`:`true or false to make it loop`
        :returns:
            `service_object_path`:`the service object path reference`
    """
    get_sysd_manager(bus=get_sys_bus()).GetUnit(
        service_name,
        reply_handler=processor.handle_get_unit_callback,
        error_handler=processor.handle_raise_error
    )
    # return false to not loop
    return loop


class ServiceStatusJob(Job):

    def __init__(self, service_name: str, processor: ServiceStatusProcessor, delay: int = 0, loop=False):
        super().__init__(_find_service_unit, delay, loop)
        self._add_args(service_name, processor)
