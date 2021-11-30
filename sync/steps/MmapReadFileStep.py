import mmap
from datetime import datetime

from core.scheduler import Scheduler
from parser.LogParser import LogGroups, LogPatterns
from parser.StringParser import Parser


class FileHandler:

    def __init__(self):
        self.force_exit = False
        self.is_active = False

    def seek_to_end_and_tail(self, filename):
        self.is_active = True
        file = FileHandler.mmap_io_find_and_open(filename)
        file.seek(file.size())
        Scheduler.schedule_function(self._schedule_in_loop,
                                    file,
                                    delay=500,
                                    loop=True)

    def _schedule_in_loop(self, loop, file):
        print("scheduling with force exit")
        if self.force_exit:
            return self.read_line_from_file(loop, file)
        else:
            self.force_exit = True
            self.is_active = False
            return False

    @staticmethod
    def read_line_from_file(loop, file):
        print("read_file")
        line = file.readline()
        print(f"reading line {line}")
        if FileHandler.check_codes(line):
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
            print("Logs not founds?")
            return False

    @staticmethod
    def mmap_io_find_and_open(filename):
        print("opening filename")
        with open(filename, mode="r", encoding="utf-8") as file_obj:
            return mmap.mmap(file_obj.fileno(), length=0, access=mmap.ACCESS_READ)
