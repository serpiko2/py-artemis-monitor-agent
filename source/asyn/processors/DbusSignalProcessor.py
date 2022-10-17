import logging

from source.core.manager import SystemBusSysd
from source.core.pubsub.Sink import Sink
from source.core.pubsub.Source import Source
from source.asyn.jobs.PropertyJob import PropertyJob
from source.asyn.models.UnitProperties import UnitProperties
from source.core.pubsub.EventsType import EventsType


class DbusSignalProcessor(Sink, Source):
    _logger = logging.getLogger(__name__)

    def __init__(self):
        super().__init__()
        self.unit_properties = UnitProperties()
        self.subscriber.subscribe(EventsType.UnitFound, self.publisher,
                                  callback=lambda object_unit:
                                  self.read_properties(object_unit))
        self.subscriber.subscribe(EventsType.ExecStartRead, self.publisher,
                                  callback=lambda exec_start: self.set_property(self.unit_properties.set_exec_start,
                                                                                exec_start))
        self.subscriber.subscribe(EventsType.LoadStateRead, self.publisher,
                                  callback=lambda load_state: self.set_property(self.unit_properties.set_load_state,
                                                                                load_state))
        self.subscriber.subscribe(EventsType.ActiveStateRead, self.publisher,
                                  callback=lambda active_state: self.set_property(self.unit_properties.set_active_state,
                                                                                  active_state))

    @classmethod
    def read_properties(cls, unit_object):
        cls._logger.debug(f"reading service properties={unit_object}")
        unit_object = SystemBusSysd.get_proxy_from_object_path(unit_object)
        service_properties = SystemBusSysd.get_properties_interface(unit_object)
        PropertyJob.get_active_state(service_properties)
        PropertyJob.get_exec_start(service_properties)
        PropertyJob.get_load_state(service_properties)

    def set_property(self, set_function: callable, value):
        set_function(value)
        if self.unit_properties.all_read():
            self._logger.info(f"Got all unit properties read with values={self.unit_properties.__repr__()}")
            self.publisher.publish(EventsType.ReadsDone, self.unit_properties)
