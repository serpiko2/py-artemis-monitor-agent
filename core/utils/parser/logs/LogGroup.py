from datetime import datetime

from core.utils.parser.RegexGroup import RegexGroup


class LogTimestampPattern:
    pattern = "%Y-%m-%d %H:%M:%S,%f"


class LogGroup(RegexGroup):

    def __init__(self,
                 timestamp: datetime = None,
                 log_level: str = None,
                 logging_class: str = None,
                 message: str = None,
                 line: str = None):
        self.timestamp = timestamp
        self.log_level = log_level
        self.logging_class = logging_class
        self.message = message
        self.line = line

    def partial_eq(self, other):
        if isinstance(other, LogGroup):
            return self.timestamp == other.timestamp \
                   or self.log_level == other.log_level \
                   or self.logging_class == other.logging_class \
                   or self.message == other.message

    def __eq__(self, other):
        if isinstance(other, LogGroup):
            return self.timestamp == other.timestamp \
                   and self.log_level == other.log_level \
                   and self.logging_class == other.logging_class \
                   and self.message == other.message

    @staticmethod
    def build(time_str: str,
              log_level: str,
              logging_class: str,
              message: str,
              line: str):
        timestamp = datetime.strptime(time_str, LogTimestampPattern.pattern)
        return LogGroup(timestamp, log_level, logging_class, message, line)
