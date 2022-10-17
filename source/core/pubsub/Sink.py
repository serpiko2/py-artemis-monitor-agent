from source.core.pubsub.Events import Subscriber


class Sink:

    def __init__(self):
        super().__init__()
        self.subscriber = Subscriber()