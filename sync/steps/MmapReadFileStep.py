from datetime import datetime

from core.scheduler import Scheduler
from parser.LogParser import LogGroups, LogPatterns
from parser.StringParser import Parser


class FileHandler:

    def __init__(self):
        self._force_exit = False
        self._is_active = False

    def force_exit(self):
        if self._is_active:
            self._force_exit = True
            print(f"forcing exit {self._force_exit}, with active state {self._is_active}")

    def seek_to_end_and_tail(self, filename):
        print(f"scheduling new handler for {filename}")
        self._is_active = True
        file = FileHandler.mmap_io_find_and_open(filename)
        # file.seek(file.size())
        Scheduler.schedule_function(self._schedule_in_loop,
                                    file,
                                    delay=2,
                                    loop=True)

    def _schedule_in_loop(self, loop, file):
        print(f"scheduled function run, status: _force_exit={self._force_exit}, "
              f"_is_active={self._is_active}")
        if not self._force_exit:
            self._is_active = self.read_line_from_file(loop, file)
            return self._is_active
        else:
            print(f"Exit Forced {self._force_exit}, with active state {self._is_active}")
            self._force_exit = False
            self._is_active = False
            return False

    @staticmethod
    def read_line_from_file(loop, file):
        print(f"read_file {file}")
        line = file.readline()
        print(f"reading line {line}")
        if FileHandler.check_codes(str(line)):
            loop = False
            print(f"ending loop on")
        return loop

    @staticmethod
    def compare_line_marker(line: str, marker: LogGroups):
        log_groups = Parser.parse_string(line, clazz=LogGroups, regex=LogPatterns.regex_pattern)
        if marker.partial_eq(log_groups):
            return log_groups

    @staticmethod
    def compare_line_timestamp(line: str, timestamp: datetime):
        return FileHandler.compare_line_marker(line, LogGroups(timestamp=timestamp))

    @staticmethod
    def check_codes(message):
        if "AMQ224097" in message:
            if "FAILED TO SETUP the JDBC Shared State NodeId" in message:
                print("Connection to database failed while setting up Jdbc Shared State NodeId, restarting service")
                print("Connection to database failed while setting up Jdbc Shared "
                      "State NodeId, restarting service")
                return False
        elif "AMQ221043" in message:
            print("Artemis initialized correctly")
            return True
        else:
            return False

    @staticmethod
    def mmap_io_find_and_open(filename):
        return open(filename, mode="r", encoding="utf-8")
