import re

from core.utils.parser.StringParser import Parser, Groups
from core.utils.parser.comparables.LogComparable import LogComparable
from core.utils.parser.logs.LogGroups import LogGroups


class LogPatterns:
    timestamp_pattern = "%Y-%m-%d %H:%M:%S,%f"

    timestamp_regex = r'(\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}\,\d{3})'
    log_level_regex = r'\s*([A-Z]*)'
    logging_class_regex = r'\s*(\[.*])'
    message_regex = r'\s*(.*)'

    regex_pattern = timestamp_regex + log_level_regex + logging_class_regex + message_regex


class LogParser(Parser):

    @staticmethod
    def parse(line: str, clazz: LogGroups, regex: str) -> Groups:
        groups = re.search(regex, line).groups()
        return clazz.build(*groups)

    @staticmethod
    def search_timestamps(group: LogGroups, comparable: LogComparable) -> ():
        found_labels = []
        for label in comparable.labels:
            if label in group.message:
                found_labels.append(label)
        return found_labels

    @staticmethod
    def search_message_for_labels(group: LogGroups, comparable: LogComparable) -> ():
        found_labels = []
        for label in comparable.labels:
            if label in group.message:
                found_labels.append(label)
        return found_labels
