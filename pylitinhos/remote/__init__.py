from .model import *
from ..db.Data import Data
from ..db.UserDAO import UserDAO


class GameManager(object):

    def __init__(self, **kw):
        self.db = kw.get('db', None)
        if self.db is None:
            self.db = Data()

        self.room_observers = {}

    def authenticate_user(self, username, password):
        user_authenticated = self.db.users.verify(username, password)
        if user_authenticated:
            return Response()
        else:
            if self.db.users.exist(username):
                return Response(error=Error(Error.Causes.InvalidLogin))
            else:
                return Response(error=Error(Error.Causes.NewUser))

    def register_new_player(self, username, password, nickname):
        '''Cria um novo usuário'''
        try:
            self.db.users.create(username, password, nickname=nickname)
            return Response()
        except:
            return Response(error=Error(Error.Causes.CreationError))

    def get_room(self, room_name):
        return Response(bundle=Bundle(room=self.db.rooms.get(room_name)))

    def room_exist(self, room_name):
        exist = self.db.rooms.exist(room_name)
        return Response(bundle=Bundle(exist=exist))

    def add_player_to_room(self, player_name, room_name):
        player = self.db.rooms.add_player(room_name, player_name)

        if room_name in self.room_observers:
            for observer in self.room_observers[room_name]:
                observer.on_add_player(player, room_name)

        return Response(bundle=Bundle(player=player))

    def observe_room(self, room_name, observer):
        if not observer:
            return

        if room_name not in self.room_observers:
            self.room_observers[room_name] = []

        self.room_observers[room_name].append(observer)
