class EventsType:

    class Jobs:
        UnitSearch = "Jobs.Event.UnitSearch"
        UnitFound = "Jobs.Event.UnitFound"
        LoadStateRead = "Jobs.Event.LoadStateRead"
        ActiveStateRead = "Jobs.Event.ActiveStateRead"
        ExecStartRead = "Jobs.Event.ExecStartRead"
        ReadsDone = "Jobs.Event.ReadsDone"
        TriggerRestart = "Jobs.Event.TriggerRestart"
        RestartJobQueued = "Jobs.Event.RestartJobQueued"

    class Dbus:
        UnitRestarted = "Dbus.Signal.UnitRestarted"
