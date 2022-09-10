class EventCollector:
    def __init__(self):
        self._events = []

    @property
    def events(self):
        return self._events

    def collect_new_events(self):
        while self._events:
            yield self._events.pop(0)