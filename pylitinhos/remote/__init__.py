from .model import *


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

        room.add_player(Player(name=player_name))

        return Response()
