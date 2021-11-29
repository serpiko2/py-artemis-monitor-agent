from parser.StringParser import Groups
from datetime import datetime


class LogPatterns:
    timestamp_pattern = "%Y-%m-%d %H:%M:%S,%f"

    timestamp_regex = r'(\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}\,\d{3})'
    log_level_regex = r'\s*([A-Z]*)'
    logging_class_regex = r'\s*(\[.*])'
    message_regex = r'\s*(.*)'

    regex_pattern = timestamp_regex + log_level_regex + logging_class_regex + message_regex


class LogGroups(Groups):

    def __init__(self, timestamp: datetime = None, log_level=None, logging_class=None, message=None):
        self.timestamp = timestamp
        self.log_level = log_level
        self.logging_class = logging_class
        self.message = message

    def partial_eq(self, other):
        if isinstance(other, LogGroups):
            return self.timestamp == other.timestamp \
                   or self.log_level == other.log_level \
                   or self.logging_class == other.logging_class \
                   or self.message == other.message

    def __eq__(self, other):
        if isinstance(other, LogGroups):
            return self.timestamp == other.timestamp \
                   and self.log_level == other.log_level \
                   and self.logging_class == other.logging_class \
                   and self.message == other.message

    @staticmethod
    def build(time_str: str, log_level: str, logging_class: str, message: str):
        timestamp = datetime.strptime(time_str, LogPatterns.timestamp_pattern)
        return LogGroups(timestamp, log_level, logging_class, message)
