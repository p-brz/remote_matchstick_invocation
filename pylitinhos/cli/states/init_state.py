import sys
import Pyro4
from ..smlite.base import State
from pylitinhos.remote.model import *


class InitState(State):

    def run(self, arguments={}):
        Pyro4.config.SERIALIZER = 'pickle'
        self.player.proxy = Pyro4.Proxy("PYRONAME:gameserver.pyro")

        self.player.name, self.player.room_name = self.register_player(
            self.player.proxy
        )

        return False

    def register_player(self, proxy):
        registered = False

        name = None
        room_name = None

        while not registered:
            name = input("Qual seu nome?\n")
            room_name = input("Sala de jogo\n")

            response = proxy.registerPlayer(name, room_name)

            if response.is_ok():
                registered = True
            else:
                if response.get_cause == Error.Causes.PlayerAlreadyOnRoom:
                    print("Nome de usuário inválido! Escolha outro.")
                else:
                    print("Error: ", response.error_msg())

        return (name, room_name)
