import dbus

from _agent.events.Events import Publisher
from _agent.events.EventsType import EventsType
from _agent.exception.UnitNotFoundException import UnitNotFoundException
from _agent.manager import Sysd
from _agent.jobs.scheduler.Job import Job


class FindPropertiesJob(Job):

    @staticmethod
    def execute(loop: bool, callback: callable, fallback: callable, service_name: str):
        """Find the service unit by it's name.
            :param:
                `name`:`the formatted service name as {name}.service`
                `loop`:`true or false to make it loop`
            :returns:
                `service_object_path`:`the service object path reference`
        """
        Sysd.get_sysd_manager().GetUnit(
            service_name,
            reply_handler=callback,
            error_handler=fallback
        )
        # return false to not loop
        return loop

    def __init__(self,
                 publisher: Publisher,
                 service_name: str,
                 delay: int = 0,
                 loop: bool = False):
        super().__init__(delay, loop, service_name)
        self.service_name = service_name
        self.publisher = publisher

    def callback(self, unit: dbus.ObjectPath):
        """handle the get unit callback for monitoring.
            :param:
                `unit`:`the unit object path`
        """
        if unit:
            unit_object = Sysd.get_proxy_from_object_path(unit)
            service_properties = Sysd.get_properties_interface(unit_object)
            self.publisher.publish(EventsType.Jobs.UnitFound, service_properties)
        else:
            raise UnitNotFoundException(self.__hash__())

    def fallback(self, e):
        print(f"async client {self} status: ExceptionRaise {e}")
        # if an error happens on read i don't need to quit
        # loop.quit()
