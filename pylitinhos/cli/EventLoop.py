
from pylitinhos.model.Event import *
from queue import Queue

class EventLoop(object):
    def __init__(self, *k, **kw):
        self.queue = Queue()

    def events(self):
        while True:
            event = self.queue.get()

            if event is None or event.type == EventTypes.Shutdown:
                break

            yield event

            self.queue.task_done()

    def stop(self, now=False):
        if now:
            with self.queue.mutex:
                self.queue.clear()
        else:
            self.queue.put(Event(EventTypes.Shutdown))
