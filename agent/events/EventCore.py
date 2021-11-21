from agent.events.UnitCheck.EventsType import Events


subscribers = dict()


def subscribe(event_type: Events, fun, nested):
    if event_type not in subscribers:
        subscribers[event_type] = []
    subscribers[event_type].append({"fun": fun, "nested": nested})


def post(event_type: Events, data):
    if event_type not in subscribers:
        return
    for fn in subscribers[event_type]:
        fn["fun"](data, fn["nested"])
