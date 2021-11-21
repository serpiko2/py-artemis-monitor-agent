from agent.events.Events import Publisher, Subscriber
from agent.events.UnitCheck.EventsType import EventsType


class PropertiesListener(Subscriber):

    def update(self, message):
        print('{} got message from PROPERTY "{}"'.format(self.name, message))

    def subscribe(self, event: EventsType.LoadStateRead, publisher: Publisher, callback):
        super().subscribe(event, publisher, callback=callback)