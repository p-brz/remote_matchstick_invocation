#!/usr/bin/python
# -*- coding: utf-8 -*-

import Pyro4

from pylitinhos.remote import GameManager
from pylitinhos.remote.model import *


def main():
    Pyro4.config.SERIALIZERS_ACCEPTED.add('pickle')
    Pyro4.config.SERIALIZER = 'pickle'

    pyroDaemon = Pyro4.Daemon()
    gameManager = GameManager()
    uri = pyroDaemon.register(gameManager)

    print("Started object at uri: ", uri)

    nameServer = Pyro4.locateNS()
    nameServer.register("gameserver.pyro", uri)

    print("registered on nameServer")

    pyroDaemon.requestLoop()

if __name__ == "__main__":
    main()
