from source.core.pubsub.Events import Publisher
from source.core.pubsub.EventsType import EventsType


class Source:
    publisher = Publisher(EventsType.__dict__.values(), "internal-channel")
