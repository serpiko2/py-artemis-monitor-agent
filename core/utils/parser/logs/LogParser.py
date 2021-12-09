import re
from typing import Type

from core.utils.parser.Parser import Parser
from core.utils.parser.logs.LogGroup import LogGroups


class LogPatterns:
    timestamp_regex = r'(\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}\,\d{3})'
    log_level_regex = r'\s*([A-Z]*)'
    logging_class_regex = r'\s*(\[.*])'
    message_regex = r'\s*(.*)'
    regex_pattern = timestamp_regex + log_level_regex + logging_class_regex + message_regex


class LogParser(Parser):

    @staticmethod
    def parse(line: str,
              clazz: LogGroups = Type[LogGroups],
              regex: str = LogPatterns.regex_pattern
              ) -> LogGroups:
        groups = re.search(regex, line).groups()
        return clazz.build(*groups)
