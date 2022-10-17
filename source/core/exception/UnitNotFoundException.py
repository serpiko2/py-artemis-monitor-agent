from source.core.exception.ApplicationException import ApplicationException


class UnitNotFoundException(ApplicationException):
    def __init__(self, message, obj, critical=True):
        self.message = message
        self.critical = critical
        self.obj = obj
