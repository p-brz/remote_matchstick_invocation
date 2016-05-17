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
from ..InputReader import InputAsync

class WaitStartState(State):

    def __init__(self, *k, **kw):
        super(WaitStartState, self).__init__(*k, **kw)
        self.evLoop = EventLoop()

    def run(self, arguments={}):
        print()
        room_name = self.player.room_name
        res = self.player.proxy.get_room(room_name)
        room = res.bundle.get_data('room')

        print(text_primary("> Sala %s <" % room_name))
        print(text_info("Total de jogadores: "), end='')
        print(room.player_count())
        print(text_info("Aguardando jogadores... "))

        self.wait_game_start()

        print()
        print(text_success("Iniciando partida..."))
        return ('game',{'event_loop' : self.evLoop})

    def wait_game_start(self):
        print(text_info("Para iniciar o jogo, digite 'start' "
                        "a qualquer momento"))
        self.observerThread = ObserverThread(self.evLoop.queue, self.player.proxy, self.player.room_name)
        #Modificar inputAsync
        self.inputAsync = InputAsync(self.evLoop.queue, "\n")

        try:
            self.observerThread.start()
            self.inputAsync.start()

            self.event_loop()
        finally:
            self.observerThread.stop()
            self.inputAsync.stop()

    def event_loop(self):
        for evt in self.evLoop.events():
            keep_going = self.on_event(evt)
            if not keep_going:
                break


    def on_event(self, event):
        # print("Event: ", event)
        if(event.type == EventTypes.AddedUser):
            self.on_added_player(event)

        elif(event.type == EventTypes.NewGame):
            return False

        elif(event.type == EventTypes.UserInput):
            #implementação penas para debug
            #TODO: permitir usuário enviar comando para começar jogo
            if event.data['line'] == 'start':
                ok = self.player.proxy.can_start_game(self.player.room_name)
                if ok:
                    self.player.proxy.start_game(self.player.room_name)
                else:
                    print(text_danger("O número de jogadores é insuficiente "
                                      "para se começar uma partida"))

            self.inputAsync = InputAsync(self.evLoop.queue, "")
            self.inputAsync.start()

        return True

    def on_added_player(self, event):
        player_name = event.data.get('player_name', '')
        print(text_success("Um novo jogador entrou na sala: "),
              player_name)

        res = self.player.proxy.get_room(self.player.room_name)
        if res.is_ok():
            room = res.bundle.get_data('room')
            print(text_info("Total de jogadores: "), end='')
            print(room.player_count())
        else:
            print("Oh noes")

class ObserverThread(Thread):
    class GameStartObserver(object):
        def __init__(self, game_manager, queue):
            self.done = False
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
