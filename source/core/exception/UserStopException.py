class UserStopException(Exception):
    def __init__(self, message="User manual Stop", obj=None, critical=True):
        self.message = message
        self.critical = critical
        self.obj = obj


