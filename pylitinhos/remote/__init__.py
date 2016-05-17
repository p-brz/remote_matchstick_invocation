from .model import *
from ..db.Data import Data
from ..db.UserDAO import UserDAO
from pylitinhos.model.Event import *

from sqlalchemy.orm.exc import NoResultFound

from concurrent.futures import ThreadPoolExecutor
import threading


class GameManager(object):

    def __init__(self, **kw):
        self.db = kw.get('db', None)
        if self.db is None:
            self.db = Data()

        self.room_observers = {}
        self.room_infos = {}
        self.executor = ThreadPoolExecutor(max_workers=2)

    def echo(self):
        return True

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

    def get_match_info(self, room_name):
        room = self.db.rooms.get(room_name).clone()
        names = room.get_players_names()
        infos = {}
        for name in names:
            player = room.get_player(name=name)
            infos.update({name: player.palitos})
        return Response(bundle=Bundle(match=infos))

    def set_ready(self, room_name, player_name):
        room = self.db.rooms.get(room_name).clone()
        player = room.get_player(player_name)

        player.ready = True
        self.check_all_ready(room_name)

    def check_all_ready(self, room):
        room = self.db.rooms.get(room_name).clone()
        names = room.get_players_names()
        all_ready = True
        for name in names:
            player = room.get_player(name=name)
            if not player.ready:
                all_ready = False
                break

        if all_ready:
            self.setup_game()


    def setup_game(self, room_name):
        self.room_infos.update({
            room_name: {
                'current_turn': 1,
                'order': room.get_players_names()
            }
        })

        evt = Event(EventTypes.StartRound,
                    player_name=self.room_infos[room_name]['order'][0])
        self._notify_room_event(room_name, evt)


    def room_exist(self, room_name):
        exist = self.db.rooms.exist(room_name)
        return Response(bundle=Bundle(exist=exist))

    def add_player_to_room(self, player_name, room_name):

        player = None
        try:
            # Cria sala e player (se ja não tiverem sido criados)
            self.db.rooms.add_player(room_name, player_name)
        except NoResultFound:
            return Response(error=Error(Error.Causes.InexistentUser))

        evt = Event(EventTypes.AddedUser, player_name=player_name, room_name=room_name)
        self._notify_room_event(room_name, evt)

        return Response(bundle=Bundle(player=player))

    def can_start_game(self, room_name):
        room = self.db.rooms.get(room_name).clone()
        return room.player_count() >= 2

    def start_game(self, room_name):
        print("Starting game")
        evt = Event(EventTypes.NewGame, valid=True)
        self._notify_room_event(room_name, evt)

    def observe_room(self, room_name, observer):
        if not observer:
            return Response(error=Error(Error.Causes.NoObserver))

        if room_name not in self.room_observers:
            self.room_observers[room_name] = []

        self.room_observers[room_name].append(observer)

        return Response()

    def _notify_room_event(self, room_name, evt):
        def notify_room_event_async(self, evt, observers):
            if observers:
                print("notify evt async : ", evt, " for %d observers" % len(observers))
                for observer in observers:
                    observer.on_event(evt)

        observers = self.room_observers.get(room_name, None)

        if observers:
            self.executor.submit(notify_room_event_async, self, evt, observers)
