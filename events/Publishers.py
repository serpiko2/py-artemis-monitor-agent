from events.pubsub.Events import Publisher

_publishers = {}


def add_publisher(name: str, publisher: Publisher):
    _publishers[name] = publisher


def get_publisher(name: str):
    return _publishers[name]
