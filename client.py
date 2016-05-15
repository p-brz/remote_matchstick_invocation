import sys
import Pyro4

from model import *

def main():
    Pyro4.config.SERIALIZER = 'pickle'
    proxy = Pyro4.Proxy("PYRONAME:gameserver.pyro")

    name = input("Qual seu nome?\n")
    room = input("Sala de jogo\n")

    response = proxy.registerPlayer(name, room)

    print("response: ", response)

    if not response.is_ok():
        print("Erro!")
        return


if __name__=="__main__":
    main()
