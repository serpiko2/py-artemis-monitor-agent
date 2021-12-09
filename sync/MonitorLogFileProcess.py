import io

from core.scheduler.Scheduler import Scheduler
from core.utils.parser.comparables.LogComparable import LogComparable, LogCompareOperations
from core.utils.parser.logs.LogParser import LogParser


class ProcessStoppingException(Exception):
    """"""


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
        print(f"Stopping monitoring for service={self.service_name} on filepath={self.filepath}")
        if self._is_active:
            self._is_stopping = True
            return self._is_stopping

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
            log_groups = LogParser.parse(line)
            fail_log_comparable = LogComparable(labels=self.fail_strings)
            success_log_comparable = LogComparable(labels=self.success_strings)
            LogCompareOperations.
        else:
            self._is_stopping = False
            self._is_active = False
            print(f"Stopped monitoring for service={self.service_name} on filepath={self.filepath}")
        return self._is_active
