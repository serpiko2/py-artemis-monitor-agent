from abc import ABC, abstractmethod


class Publisher:

    def __init__(self, events):
        # maps event names to subscribers
        # str -> dict
        self.events = {event: dict() for event in events}

    def get_subscribers(self, event):
        return self.events[event]

    def register(self, event, who, callback):
        self.get_subscribers(event)[who] = callback

    def unregister(self, event, who):
        del self.get_subscribers(event)[who]

    def publish(self, event, message):
        print(f"publishing event {event} with message {message}")
        for subscriber, callback in self.get_subscribers(event).items():
            callback(message)


class _Subscriber(ABC):

    def __init__(self, name):
        self.name = name

    def _update(self, message):
        print('{} got message "{}"'.format(self.name, message))

    @abstractmethod
    def _subscribe(self, event, publisher: Publisher, callback=_update):
        publisher.register(event, self, callback=callback)


class Subscriber(_Subscriber):

    def update(self, message):
        print('{} got message "{}"'.format(self.name, message))

    def subscribe(self, event, publisher: Publisher, callback=update):
        publisher.register(event, self, callback=callback)

    def _update(self, message):
        super()._update(message)

    def _subscribe(self, event, publisher: Publisher, callback=_update):
        super()._subscribe(event, publisher, callback)
