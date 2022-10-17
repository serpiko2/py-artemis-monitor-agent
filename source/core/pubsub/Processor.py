from source.core.pubsub.Sink import Sink
from source.core.pubsub.Source import Source


class Processor(Sink, Source):

    def __init__(self):
        super().__init__()
