import logging

from source.asyn.jobs.Job import Job
from source.core.manager import SystemBusSysd
from source.core.pubsub.EventsType import EventsType


class ServiceJob(Job):
    _logger = logging.getLogger(__name__)

    @classmethod
    def _reply(cls, *args):
        cls._logger.debug(f"{ServiceJob.__name__} got reply f{args}")
        cls.publisher.publish(EventsType.UnitFound, *args)

    @classmethod
    def _error(cls, *args):
        cls._logger.error(f"{ServiceJob.__name__} got error f{args}")

    @classmethod
    def get_service_object_path(cls, service_name: str,
                                reply_cb=_reply, error_cb=_error):
        return SystemBusSysd.get_sysd_manager().GetUnit(
            service_name,
            reply_handler=reply_cb,
            error_handler=error_cb,
        )
