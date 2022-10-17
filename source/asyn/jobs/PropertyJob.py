import logging

from source.asyn.jobs.Job import Job
from source.core.manager.consts.Interfaces import Interfaces
from source.core.manager.consts.Properties import Properties
from source.core.pubsub.EventsType import EventsType


class PropertyJob(Job):
    _logger = logging.getLogger(__name__)

    @classmethod
    def get_active_state(cls, service_properties):
        return cls._get_property(service_properties,
                                 Interfaces.Unit,
                                 Properties.ActiveState,
                                 EventsType.ActiveStateRead)

    @classmethod
    def get_load_state(cls, service_properties):
        return cls._get_property(service_properties,
                                 Interfaces.Unit,
                                 Properties.LoadState,
                                 EventsType.LoadStateRead)

    @classmethod
    def get_exec_start(cls, service_properties):
        return cls._get_property(service_properties,
                                 Interfaces.Service,
                                 Properties.ExecStart,
                                 EventsType.ExecStartRead)

    @classmethod
    def _get_property(cls, service_properties, interface, prop, event):
        return service_properties.Get(
            interface, prop,
            reply_handler=lambda message: cls._reply(event, message),
            error_handler=cls._error,
        )

    @classmethod
    def _reply(cls, event, message):
        cls._logger.debug(f"{cls.__name__} event={event} got reply={message}")
        cls.publisher.publish(event, message)

    @classmethod
    def _error(cls, *args):
        cls._logger.error(f"{cls.__name__} got error f{args}")
