import io
import logging

from source.core.parser.comparables.LogComparable import LogComparable, LogCompareOperations
from source.core.parser.logs.LogParser import LogStringParser
from source.core.pubsub.EventsType import EventsType
from source.core.pubsub.Source import Source
from source.core.scheduler.Scheduler import Scheduler


class ProcessStoppingException(Exception):
    """"""


class MonitorLogFileRunner(Source):
    logger = logging.getLogger(__name__)

    def __init__(self,
                 fail_strings,
                 success_strings,
                 file_path: str,
                 service_name: str,
                 poll_rate: int = 10,
                 encoding: str = "utf8"):
        self.fail_strings = fail_strings
        self.success_strings = success_strings
        self.service_name = service_name
        self.poll_rate = poll_rate
        self.file_path = file_path
        self.file = open(file_path, mode="r", encoding=encoding)
        self._is_stopping = False
        self._is_active = False
        self._result = False

    def stop(self):
        if self._is_active:
            self.logger.info(f"Stopping monitoring for service={self.service_name} on filepath={self.file_path}")
            self._is_stopping = True

    def start(self):
        if not self._is_stopping:
            self._result = False
            self._is_stopping = False
            self.file.seek(0, io.SEEK_END)
            self._is_active = True
            self.logger.info(f"Scheduling monitoring for service={self.service_name} "
                             f"on filepath={self.file_path} "
                             f"with pollrate={self.poll_rate}")
            Scheduler.schedule_function(self._process, poll=self.poll_rate)
        else:
            self.logger.error(f"Trying to start a process in stopping phase "
                              f"service={self.service_name} on filepath={self.file_path}")
            raise ProcessStoppingException

    def _process(self):
        if not self._is_stopping:
            line = self.file.readline()
            log_groups = LogStringParser.parse(line)
            if log_groups:
                if self._check_for_failure(log_groups):
                    # fail flow - try a restart
                    self.logger.info(f"Start fail for service={self.service_name}. Trying to Restart")
                    self.publisher.publish(EventsType.TriggerRestart, self.service_name)
                    self._result = False
                elif self._check_for_success(log_groups):
                    # success flow - notify success and stop
                    self.logger.info(f"Start success for service={self.service_name}. Going to Sleep")
                    self.publisher.publish(EventsType.StartSuccess, "Start success! Going to Sleep")
                    self._result = True
        else:
            self._is_stopping = False
            self._is_active = False
            self.logger.info(f"Stopped monitoring for service={self.service_name} on filepath={self.file_path}")
        return self._is_active

    def _check_for_failure(self, log_groups):
        fail_log_comparable = LogComparable(labels=self.fail_strings)
        return LogCompareOperations.is_labels_in_message(log_groups, fail_log_comparable)

    def _check_for_success(self, log_groups):
        success_log_comparable = LogComparable(labels=self.success_strings)
        return LogCompareOperations.is_labels_in_message(log_groups, success_log_comparable)

    def is_success(self):
        if not self._is_active and not self._is_stopping:
            return self._result
        else:
            return False
