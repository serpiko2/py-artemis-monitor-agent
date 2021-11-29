class UnitNotFoundException(Exception):
    def __init__(self, obj):
        self.obj = obj
