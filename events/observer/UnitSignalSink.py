from core.manager import SessionBusSysd
from events.observer.Events import Publisher
from events.observer.EventsType import EventsType


class UnitSignalSink:

    def handle(self, message):
        print("got message, ", message)
        self.publisher.publish(EventsType.Dbus.UnitRestarted, message)

    def __init__(self, publisher: Publisher, callback=handle):
        self.callback = callback
        self.publisher = publisher
        self._register()

    def _register(self):
        SessionBusSysd.connect_to_signal(signal="Unit", callback=self.callback)
