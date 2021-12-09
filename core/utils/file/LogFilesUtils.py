from datetime import datetime

from core.utils.parser.Parser import Parser
from core.utils.parser.logs.LogParser import LogGroups, LogPatterns, LogParser


class LogFilesUtils:

    @staticmethod
    def elaborate_line(looping: bool, line: str):
        print(f"reading line {line}")
        result = LogParser.parse(line)
        if result == "Failed":
            looping = False
            print(f"ending loop on failure, restarting")
        elif result == "Success":
            looping = False
            print(f"ending loop on success, doing nothing")
        return looping

    @staticmethod
    def compare_line_marker(line: str, marker: LogGroups):
        log_groups = Parser.parse(line, clazz=LogGroups, regex=LogPatterns.regex_pattern)
        if marker.partial_eq(log_groups):
            return log_groups

    @staticmethod
    def compare_line_timestamp(line: str, timestamp: datetime):
        return LogFilesUtils.compare_line_marker(line, LogGroups(timestamp=timestamp))

    @staticmethod
    def compare_labels(line: str, labels):
        marker = LogGroups(message="")
        log_groups = LogParser.parse_string(line, clazz=LogGroups, regex=LogPatterns.regex_pattern)
        log_groups.filter_for(marker, lambda item, comparable: comparable)
        if "AMQ224097" in line:
            if "FAILED TO SETUP the JDBC Shared State NodeId" in line:
                print("Connection to database failed while setting up Jdbc Shared State NodeId, restarting service")
                print("Connection to database failed while setting up Jdbc Shared "
                      "State NodeId, restarting service")
                return "Failed"
        elif "AMQ221000" in line:
            print("Artemis initialized correctly")
            return "Success"
        else:
            return "Pass"