from agent.events.UnitCheck.ServiceStatusProcessor import ServiceStatusProcessor
from agent.manager.DbusManager import get_sys_bus, get_sysd_manager
from agent.scheduler import Scheduler
from agent.scheduler.Scheduler import Job

class ServiceStatusJob(Job):

    def __init__(self, service_name, processor: ServiceStatusProcessor, delay: int=0, loop=False):
        super().__init__(_find_service_unit, delay)
        self.processor = processor
        self.loop = loop
        self.service_name = service_name

    def schedule(self):
        Scheduler.schedule_function(self.func, self.delay, self.service_name, self.processor, self.loop)

def _find_service_unit(service_name, processor, loop):
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
