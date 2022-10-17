import logging
from typing import List

from source.core.parser.comparables.TimestampComparable import TimestampComparable
from source.core.parser.logs.LogGroup import LogGroup


class LogComparable:
    def __init__(self,
                 timestamps: TimestampComparable = None,
                 log_levels: List[str] = None,
                 logging_classes: List[str] = None,
                 labels: List[str] = None):
        self.timestamps = timestamps
        self.log_levels = log_levels
        self.logging_classes = logging_classes
        self.labels = labels


class LogCompareOperations:
    _logger = logging.getLogger(__name__)

    @classmethod
    def is_timestamp_in_range(cls, comparable: LogComparable, group: LogGroup) -> ():
        raise NotImplemented

    @classmethod
    def get_labels_in_message(cls, comparable: LogComparable, group: LogGroup) -> List[str]:
        found_labels = []
        for label in comparable.labels:
            cls._logger.debug(f"Searching label={label} in group={group.__dict__}")
            if label.find(group.message) != -1:
                found_labels.append(label)
        return found_labels

    @classmethod
    def is_labels_in_message(cls, group: LogGroup, comparable: LogComparable) -> bool:
        for label in comparable.labels:
            cls._logger.debug(f"Searching label={label} in group={group.__dict__}")
            if label in group.message:
                return True
        return False
