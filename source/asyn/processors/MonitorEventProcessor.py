from source.core.pubsub.EventsType import EventsType
from source.core.pubsub.Sink import Sink
from source.core.pubsub.Source import Source


class MonitorEventProcessor(Sink, Source):

    def __init__(self, monitor_start_cb, monitor_stop_cb):
        super().__init__()
        self.subscriber.subscribe(EventsType.ProcessLogStart, self.publisher,
                                  callback=monitor_start_cb)
        self.subscriber.subscribe(EventsType.ProcessLogStop, self.publisher,
                                  callback=monitor_stop_cb)
        self.subscriber.subscribe(EventsType.TriggerRestart, self.publisher,
                                  callback=monitor_stop_cb)
        self.subscriber.subscribe(EventsType.StartSuccess, self.publisher,
                                  callback=monitor_stop_cb)
