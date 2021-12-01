from datetime import datetime


class TimestampComparable:
    def __init__(self,
                 before: datetime = None,
                 when: datetime = None,
                 after: datetime = None):
        self.before = before
        self.when = when
        self.after = after

