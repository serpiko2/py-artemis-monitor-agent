import logging


class Subscription:
    def __init__(self, channel_name, event, callback):
        self.channel_name = channel_name
        self.event = event
        self.callback = callback


class Publisher:

    def __init__(self, events, channel_name):
        # maps event names to subscribers
        # str -> dict
        self.channel_name = channel_name
        self.events = {event: dict() for event in events}

    def get_subscribers(self, event):
        return self.events[event]

    def register(self, event, who, callback):
        self.get_subscribers(event)[who] = callback

    def unregister(self, event, who):
        del self.get_subscribers(event)[who]

    def publish(self, event, message):
        logging.debug(f"publishing event {event} with message {message} on channel {self.channel_name}")
        for subscriber, callback in self.get_subscribers(event).items():
            callback(message)


class _Subscriber:

    def __init__(self, name):
        self.name = name

    def _update(self, message):
        print('{} got message "{}"'.format(self.name, message))

    def _subscribe(self, event, publisher: Publisher, callback=_update):
        publisher.register(event, self, callback=callback)
        return Subscription(publisher.channel_name, event, callback)


class Subscriber(_Subscriber):

    def __init__(self, name):
        super().__init__(name)

    def update(self, message):
        super()._update(message)

    def subscribe(self, event, publisher: Publisher, callback=update):
        return super()._subscribe(event, publisher, callback)


# TODO: wip
