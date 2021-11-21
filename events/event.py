from .EventsType import Events


subscribers = dict()


def subscribe(event_type: Events, fn, fn2):
    if event_type not in subscribers:
        subscribers[event_type] = []
    subscribers[event_type].append({"func": fn, "nested": fn2})


def post(event_type: Events, data):
    if event_type not in subscribers:
        return
    for fn in subscribers[event_type]:
        fn["func"](data, fn["nested"])
