import logging

from source.asyn.jobs.Job import Job
from source.core.manager import SystemBusSysd
from source.core.pubsub.EventsType import EventsType


class RestartJob(Job):
    _logger = logging.getLogger(__name__)

    @classmethod
    def restart_unit_non_blocking(cls, service_name, mode='replace'):
        cls._logger.debug(f"trying to restart unit={service_name}")
        SystemBusSysd.get_sysd_manager().RestartUnit(service_name,
                                                     mode,
                                                     reply_handler=lambda message: cls._reply(message),
                                                     error_handler=lambda error: cls._error(error))

    @classmethod
    def _reply(cls, *args):
        cls._logger.debug(f"got reply f{args}")
        cls.publisher.publish(EventsType.RestartJobQueued, "Queued restart job")

    @classmethod
    def _error(cls, *args):
        cls._logger.error(f"got error f{args}")