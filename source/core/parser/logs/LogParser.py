import re
import logging

from source.core.parser.StringParser import StringParser
from source.core.parser.logs.LogGroup import LogGroup


class LogPatterns:
    timestamp_regex = r'(\d{4}-\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}\,\d{3})'
    log_level_regex = r'\s*([A-Z]*)'
    logging_class_regex = r'\s*(\[.*])'
    message_regex = r'\s*(.*)'
    regex_pattern = timestamp_regex + log_level_regex + logging_class_regex + message_regex


class LogStringParser(StringParser):

    logger = logging.getLogger(__name__)

    @classmethod
    def parse(cls,
              line: str,
              clazz: LogGroup = LogGroup(),
              regex: str = LogPatterns.regex_pattern
              ):
        if line:
            try:
                groups = re.search(regex, line.strip()).groups()
                return clazz.build(*groups)
            except AttributeError as e:
                return None
        return None
