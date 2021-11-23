from _agent.events.Events import Publisher, Subscriber
from _agent.events.EventsType import EventsType


class ServiceStatusProcessor:

    def __init__(self, source: Publisher, sink: Subscriber):
        self.source = source
        self.sink = sink

    def publish(self):
        """
        # START Callbacks for asynchronous calls
        """

    def subscribe(self, event: EventsType, fn, cb):
        self.sink.subscribe(event, self.source, callback=lambda message: fn(message, cb))

    """
    # START Callbacks for asynchronous calls
    """


    """
    # END Callbacks for asynchronous calls
    """
