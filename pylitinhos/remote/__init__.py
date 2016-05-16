from .model import *
from ..db.Data import Data
from ..db.UserDAO import UserDAO

from sqlalchemy.orm.exc import NoResultFound

from concurrent.futures import ThreadPoolExecutor
import threading

class GameManager(object):

    def __init__(self, **kw):
        self.db = kw.get('db', None)
        if self.db is None:
            self.db = Data()

        self.room_observers = {}
        self.executor = ThreadPoolExecutor(max_workers=2)

    def destroy(self):
        self.executor.shutdown()
        self.db.destroy()

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
        return Response(bundle=Bundle(room=self.db.rooms.get(room_name).clone()))

    def room_exist(self, room_name):
        exist = self.db.rooms.exist(room_name)
        return Response(bundle=Bundle(exist=exist))

    def add_player_to_room(self, player_name, room_name):

        player = None
        try:
            #Cria sala e player (se ja não tiverem sido criados)
            self.db.rooms.add_player(room_name, player_name)
        except NoResultFound:
            return Response(error=Error(Error.Causes.InexistentUser))

        self._notify_added_player(player_name, room_name)

        return Response(bundle=Bundle(player=player))

    def observe_room(self, room_name, observer):
        if not observer:
            return Response(error=Error(Error.Causes.NoObserver))

        if room_name not in self.room_observers:
            self.room_observers[room_name] = []

        self.room_observers[room_name].append(observer)

        return Response()

    def _notify_added_player(self, player_name, room_name):
        def notify_added_player_async(self, player_name, room_name, observers):
            # print("notify_added_player_async", (player_name, room_name, observers))

            if observers:
                for observer in observers:
                    observer.on_add_player(player_name, room_name)

        observers = self.room_observers.get(room_name, None)

        if observers:
            self.executor.submit(notify_added_player_async, self, player_name, room_name, observers)
