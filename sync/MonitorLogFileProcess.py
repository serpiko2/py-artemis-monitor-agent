import io

from core.scheduler.Scheduler import Scheduler
from core.utils.parser.logs.LogParser import LogParser


class MonitorLogFileProcess:

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
        self._is_stopping = False
        self.file.seek(0, io.SEEK_END)
        self._is_active = True
        Scheduler.schedule_function(self._process, poll=self.poll_rate)

    def _process(self):
        if self._is_stopping:
            line = self.file.readline()
            log_groups = LogParser.parse(line)
            log_groups.message
        else:
            self._is_stopping = False
            self._is_active = False
        if not self._is_active:
            print(f"Stopped monitoring for service={self.service_name} on filepath={self.filepath}")
        return self._is_active
