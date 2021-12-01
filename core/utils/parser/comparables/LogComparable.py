class LogComparable:
    def __init__(self,
                 timestamps: () = None,
                 log_levels: () = None,
                 logging_classes: () = None,
                 labels: () = None):
        self.timestamps = timestamps
        self.log_levels = log_levels
        self.logging_classes = logging_classes
        self.labels = labels
