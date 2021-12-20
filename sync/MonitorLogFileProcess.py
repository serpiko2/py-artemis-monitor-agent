import io

from core.Logger import Loggable
from core.scheduler.Scheduler import Scheduler
from core.utils.parser.comparables.LogComparable import LogComparable, LogCompareOperations
from core.utils.parser.logs.LogParser import LogStringParser
from sync.steps.RestartUnitStep import RestartUnitStep


class ProcessStoppingException(Exception):
    """"""


@Loggable
class MonitorLogFileProcess:

    fail_strings = ["AMQ224097", "FAILED TO SETUP the JDBC Shared State NodeId"]
    success_strings = ["AMQ221000"]

    def __init__(self,
                 filepath: str,
                 service_name: str,
                 encoding: str = "utf8",
                 poll_rate: int = 10):
        self.service_name = service_name
        self.poll_rate = poll_rate
        self._is_stopping = False
        self._is_active = False
        self.filepath = filepath
        self.file = open(filepath, mode="r", encoding=encoding)

    def stop(self):
        self.logger.info(f"Stopping monitoring for service={self.service_name} on filepath={self.filepath}")
        if self._is_active:
            self._is_stopping = True

    def start(self):
        if not self._is_stopping:
            self._is_stopping = False
            self.file.seek(0, io.SEEK_END)
            self._is_active = True
            Scheduler.schedule_function(self._process, poll=self.poll_rate)
        else:
            raise ProcessStoppingException

    def _process(self):
        if not self._is_stopping:
            line = self.file.readline()
            log_groups = LogStringParser.parse(line)
            if self._check_for_failure(log_groups):
                # fail flow - try a restart
                RestartUnitStep.restart_unit_non_blocking(self.service_name)
                self.stop()
            elif self._check_for_success(log_groups):
                # success flow - do nothing
                self.stop()
        else:
            self._is_stopping = False
            self._is_active = False
            self.logger.info(f"Stopped monitoring for service={self.service_name} on filepath={self.filepath}")
        return self._is_active

    def _check_for_failure(self, log_groups):
        fail_log_comparable = LogComparable(labels=self.fail_strings)
        return LogCompareOperations.is_labels_in_message(log_groups, fail_log_comparable)

    def _check_for_success(self, log_groups):
        success_log_comparable = LogComparable(labels=self.success_strings)
        return LogCompareOperations.is_labels_in_message(log_groups, success_log_comparable)
