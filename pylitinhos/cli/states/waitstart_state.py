import sys
import Pyro4
import Pyro4.util
from colorama import Fore
from pylitinhos.remote.model import *
from ..color import *
from ..smlite import State
from getpass import getpass


class WaitStartState(State):
    class GameStartObserver(object):
        def __init__(self, game_manager):
            self.done = False
            self.game_manager = game_manager

        @Pyro4.callback
        @Pyro4.oneway
        def on_add_player(self, player_name, room_name):
            #TODO: corrigir implementação

            print("adicionou jogador: ", player_name, " na sala: ", room_name)

            res = self.game_manager.get_room(room_name)

            print("got response :", res)
            if res.is_ok():
                room = res.bundle.get_data('room')
                print("room :", room)
                self.done = room.player_count() > 1

        def is_done(self):
            print("is done? ", self.done)

            return self.done


    def run(self, arguments={}):
        Pyro4.config.SERIALIZERS_ACCEPTED.add('pickle')
        with Pyro4.core.Daemon() as daemon:
            # register our callback handler
            observer = self.GameStartObserver(self.player.proxy)
            daemon.register(observer)

            res = self.player.proxy.observe_room(self.player.room_name, observer)

            if not res.is_ok():
                print("failed to observe room")
                return False

            print("waiting for all work complete...")
            daemon.requestLoop(loopCondition=lambda: not observer.is_done())
            print("done!")

        return False
