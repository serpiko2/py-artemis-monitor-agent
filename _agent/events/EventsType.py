class EventsType:
    UnitSearch = "UnitSearch"
    UnitFound = "UnitFound"
    LoadStateRead = "LoadStateRead"
    ActiveStateRead = "ActiveStateRead"
    ExecStartRead = "ExecStartRead"
    ReadsDone = "ReadsDone"
    TriggerRestart = "TriggerRestart"
    RestartJobQueued = "RestartJobQueued"


def get_events():
    return EventsType.__dict__.values()

    #TODO: separate the list, create a base class and take this out