#!/usr/bin/python
# -*- coding: utf-8 -*-

import Pyro4

from pylitinhos.remote import GameManager
from pylitinhos.remote.model import *


def main():
    Pyro4.config.SERIALIZERS_ACCEPTED.add('pickle')
    pyroDaemon = Pyro4.Daemon()
    uri = pyroDaemon.register(GameManager)

    print("Started object at uri: ", uri)

    nameServer = Pyro4.locateNS()
    nameServer.register("gameserver.pyro", uri)

    print("registered on nameServer")

    pyroDaemon.requestLoop()

if __name__ == "__main__":
    main()
