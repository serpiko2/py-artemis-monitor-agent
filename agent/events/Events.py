from abc import ABC, abstractmethod

class Publisher:

    def __init__(self, events):
        # maps event names to subscribers
        # str -> dict
        self.events = { event : dict()
                          for event in events }

    def get_subscribers(self, event):
        return self.events[event]

    def register(self, event, who, callback=None):
        if callback is None:
            callback = lambda message: print('{} got message "{}"'.format(who, message))
        self.get_subscribers(event)[who] = callback

    def unregister(self, event, who):
        del self.get_subscribers(event)[who]

    def publish(self, event, message):
        for subscriber, callback in self.get_subscribers(event).items():
            callback(message)


class Subscriber(ABC):

    def __init__(self, name):
        self.name = name

    @abstractmethod
    def update(self, message):
        print('{} got message "{}"'.format(self.name, message))

    def subscribe(self, event, publisher: Publisher, callback):
        publisher.register(event, self, callback=callback)
