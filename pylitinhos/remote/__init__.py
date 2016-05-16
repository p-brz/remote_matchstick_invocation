from .model import *
from ..db.UserDAO import UserDAO


class GameManager(object):

    def __init__(self):
        self.rooms = {}

    def authenticate_user(self, username, password):
        dao = UserDAO()
        user_authenticated = dao.verify(username, password)
        if user_authenticated:
            return Response()
        else:
            user_exists = dao.get(username)
            if user_exists:
                return Response(error=Error(Error.Causes.InvalidLogin))
            else:
                return Response(error=Error(Error.Causes.NewUser))

    def registerPlayer(self, player_name, roomName):
        room = self.rooms.get(roomName, None)
        if room is None:
            room = Room(name=roomName)
            self.rooms[roomName] = room

        if room.has_player(roomName):
            return Response(error=Error(Error.Causes.PlayerAlreadyOnRoom))

        room.add_player(Player(name=player_name))

        return Response()
