from typing import List

from core.utils.parser.comparables.TimestampComparable import TimestampComparable
from core.utils.parser.logs.LogGroup import LogGroup


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

    @staticmethod
    def is_timestamp_in_range(comparable: LogComparable, group: LogGroup) -> ():
        raise NotImplemented

    @staticmethod
    def get_labels_in_message(comparable: LogComparable, group: LogGroup) -> List[str]:
        found_labels = []
        for label in comparable.labels:
            if label.find(group.message):
                found_labels.append(label)
        return found_labels

    @staticmethod
    def is_labels_in_message(group: LogGroup, comparable: LogComparable) -> bool:
        for label in comparable.labels:
            if not label.find(group.message):
                return False
        return True
