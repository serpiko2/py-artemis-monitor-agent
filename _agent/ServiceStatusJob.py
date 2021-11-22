from _agent.events.UnitCheck.ServiceStatusProcessor import ServiceStatusProcessor
from _agent.manager.DbusManager import get_sys_bus, get_sysd_manager
from _agent.scheduler.Scheduler import Job

class ServiceStatusJob(Job):

    def __init__(self, service_name, processor: ServiceStatusProcessor, delay: int=0, loop=False):
        super().__init__(self._find_service_unit, delay)
        self.processor = processor
        self.loop = loop
        self.service_name = service_name

    def _find_service_unit(self):
        """Find the service unit by it's name.
            :param:
                `name`:`the formatted service name as {name}.service`
                `loop`:`true or false to make it loop`
            :returns:
                `service_object_path`:`the service object path reference`
        """
        get_sysd_manager(bus=get_sys_bus()).GetUnit(
            self.service_name,
            reply_handler=self.processor.handle_get_unit_callback,
            error_handler=self.processor.handle_raise_error
        )
        # return false to not loop
        return self.loop
