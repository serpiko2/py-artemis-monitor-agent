import io
from typing import TextIO

from core.scheduler import Scheduler
from core.utils.file.LogFilesUtils import LogFilesUtils


class MonitorLogFileProcess:

    def __init__(self, file_path: str, encoding: str = "utf8"):
        self._force_exit = False
        self._is_active = False
        self.file_path = file_path
        self.file = open(file_path, mode="r", encoding=encoding)

    def force_exit(self):
        if self._is_active:
            self._force_exit = True
            print(f"forcing exit {self._force_exit}, with active state {self._is_active}")

    def seek_to_end_and_tail(self, file_path: str):
        print(f"scheduling new handler for {file_path}")
        self._is_active = True
        self.file.seek(0, io.SEEK_END)
        Scheduler.schedule_function(self._schedule_in_loop,
                                    self.file,
                                    delay=10)

    def _schedule_in_loop(self, file: TextIO):
        print(f"scheduled function run, status: _force_exit={force_exit}")
        if force_exit:
            line = file.readline()
            _is_active = LogParser.parse(line)
            return _is_active
        else:
            print(f"Exit Forced {self._force_exit}, with active state {self._is_active}")
            self._force_exit = False
            self._is_active = False
        return False

