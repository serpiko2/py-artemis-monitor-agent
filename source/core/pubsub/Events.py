import logging


class Subscription:
    def __init__(self, subscriber, channel_name, event, callback: callable):
        self.subscriber = subscriber
        self.channel_name = channel_name
        self.event = event
        self.callback = callback


class Publisher:

    _logger = logging.getLogger(__name__)

    def __init__(self, events, channel_name):
        # maps event names to subscribers
        # str -> dict
        self.channel_name = channel_name
        self.events = {event: dict() for event in events}

    def get_subscribers(self, event):
        return self.events[event]

    def register(self, event, who, callback: callable) -> Subscription:
        self.get_subscribers(event)[who] = callback
        return Subscription(who, self.channel_name, event, callback)

    def unregister(self, event, who):
        del self.get_subscribers(event)[who]

    def publish(self, event, *message):
        self._logger.debug(f"publishing event {event} with message {message} on channel {self.channel_name}")
        for subscriber, callback in self.get_subscribers(event).items():
            callback.__get__(*message)()


class Subscriber:

    _logger = logging.getLogger(__name__)

    def __init__(self, name = __name__):
        self.name = name

    def _update(self, message):
        self._logger.debug('{} got message "{}"'.format(self.name, message))

    def subscribe(self, event, publisher: Publisher, callback=_update) -> Subscription:
        return publisher.register(event, self, callback=callback)