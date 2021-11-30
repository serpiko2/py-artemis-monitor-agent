import mmap
from datetime import datetime

from core.scheduler import Scheduler
from parser.LogParser import LogGroups, LogPatterns
from parser.StringParser import Parser


class FileHandler:

    @staticmethod
    def _compare_line_marker(line: str, marker: LogGroups):
        log_groups = Parser.parse_string(line, clazz=LogGroups, regex=LogPatterns.regex_pattern)
        if marker.partial_eq(log_groups):
            return log_groups

    @staticmethod
    def _compare_line_timestamp(line: str, timestamp: datetime):
        return FileHandler._compare_line_marker(line, LogGroups(timestamp=timestamp))

    @staticmethod
    def _check_codes(message):
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
    def _read_line_from_file(loop, file):
        print("read_file")
        line = file.readline()
        print(f"reading line {line}")
        if FileHandler._check_codes(line):
            loop = False
            print(f"ending loop on")
        return loop

    @staticmethod
    def _mmap_io_find_and_open(filename):
        print("opening filename")
        with open(filename, mode="r", encoding="utf-8") as file_obj:
            return mmap.mmap(file_obj.fileno(), length=0, access=mmap.ACCESS_READ)

    @staticmethod
    def seek_to_end_and_tail(filename):
        file = FileHandler._mmap_io_find_and_open(filename)
        file.seek(file.size())
        Scheduler.schedule_function(FileHandler._read_line_from_file,
                                    file, 5,
                                    delay=500,
                                    loop=True)
