 #!/usr/bin/python
 # -*- coding: utf-8 -*-

import Pyro4

from model import *

class GameManager(object):
    def __init__(self):
        self.rooms = {}

    def registerPlayer(self, player_name, roomName):
        room = self.rooms.get(roomName, None)
        if room is None:
            room = Room(name=roomName)
            self.rooms[roomName] = room

        if room.has_player(roomName):
            return Response(error=Error(Error.Causes.PlayerAlreadyOnRoom))

        room.add_player(Player(name = player_name))

        return Response()

def main():
    Pyro4.config.SERIALIZERS_ACCEPTED.add('pickle')
    pyroDaemon = Pyro4.Daemon()
    uri = pyroDaemon.register(GameManager)

    print("Started object at uri: ", uri)

    nameServer = Pyro4.locateNS()
    nameServer.register("gameserver.pyro", uri)

    print("registered on nameServer")

    pyroDaemon.requestLoop()

if __name__=="__main__":
    main()
