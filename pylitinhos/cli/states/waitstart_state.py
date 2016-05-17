import sys
import Pyro4
import Pyro4.util
from colorama import Fore
from ..color import *
from ..smlite import State
from getpass import getpass

from threading import Thread

from queue import Queue

from pylitinhos.remote.model import *
from ..EventLoop import *

class WaitStartState(State):

    def __init__(self, *k, **kw):
        super(WaitStartState, self).__init__(*k, **kw)
        self.evLoop = EventLoop()

    def run(self, arguments={}):
        self.observerThread = ObserverThread(self.evLoop.queue, self.player.proxy, self.player.room_name)
        self.observerThread.start()

        for evt in self.evLoop.events():
            self.on_event(evt)

        return False

    def on_event(self, event):
        print("Event: ", event)

class ObserverThread(Thread):
    class GameStartObserver(object):
        def __init__(self, game_manager, queue):
            self.game_manager = game_manager
            self.queue = queue

        @Pyro4.callback
        @Pyro4.oneway
        def on_event(self, evt):
            self.queue.put(evt)

    def __init__(self, queue, game_manager, room_name):
        super(ObserverThread, self).__init__()

        self.queue = queue
        self.game_manager = game_manager
        self.room_name = room_name

        self.daemon = Pyro4.core.Daemon()

    def run(self):
        observer = self.GameStartObserver(self.game_manager, self.queue)
        self.daemon.register(observer)

        res = self.game_manager.observe_room(self.room_name, observer)

        if not res.is_ok():
            print("failed to observe room")
            return

        self.daemon.requestLoop()

    def stop(self):
        self.daemon.shutdown()
