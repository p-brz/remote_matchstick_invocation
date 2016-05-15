import sys
import Pyro4

from model import *

class Client(object):
    def __init__(self):
        self.name = None
        self.room_name = None
        self.proxy = None

    def start(self):
        self.connect()
        self.register()
        self.waitStart()
        while(self.play_match()):
            pass
        self.notifyResult()

    def connect(self):
        Pyro4.config.SERIALIZER = 'pickle'
        self.proxy = Pyro4.Proxy("PYRONAME:gameserver.pyro")

    def register(self):
        registered = False

        while not registered:
            self.name = input("Qual seu nome?\n")
            self.room_name = input("Sala de jogo\n")

            response = self.proxy.registerPlayer(self.name, self.room_name)

            if response.is_ok():
                registered = True
            else :
                if response.get_cause == Error.Causes.PlayerAlreadyOnRoom:
                    print("Nome de usuário inválido! Escolha outro.")
                else:
                    print("Error: ", response.error_msg())

    def waitStart(self):
        print("wait Start")

    def play_match(self):
        return False

    def notifyResult(self):
        pass

def main():
    client = Client()
    client.start()


if __name__=="__main__":
    main()
