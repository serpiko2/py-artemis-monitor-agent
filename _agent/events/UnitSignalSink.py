from _agent.events.Events import Publisher
from _agent.events.EventsType import EventsType
from _agent.manager import Sysd


class UnitSignalSink:

    def handle(self, message):
        print("got message, ", message)
        self.publisher.publish(EventsType.Dbus.UnitRestarted, message)

    def __init__(self, publisher: Publisher, callback=handle):
        self.callback = callback
        self.publisher = publisher
        self._register()

    def _register(self):
        Sysd.connect_to_signal(signal="Unit", callback=self.callback)
