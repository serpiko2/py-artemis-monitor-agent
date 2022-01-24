class ApplicationException(Exception):
    def __init__(self, message, obj, critical=False):
        self.message = message
        self.critical = critical
        self.obj = obj
