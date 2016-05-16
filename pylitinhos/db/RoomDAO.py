from .BaseDAO import BaseDAO
from .PlayerDAO import PlayerDAO
from pylitinhos.model.Room import Room
from pylitinhos.model.Player import Player
from pylitinhos.model.User import User


class RoomDAO(BaseDAO):
    def __init__(self):
        super(RoomDAO, self).__init__(Room)

    def get_or_create(self, room_name, session=None, autocommit=True):
        s = self.build_session(session)
        room = self.get(room_name, s)
        if room is None:
            room = self.create(room_name, session, autocommit)

        return room

    def add_player(self, room_name, player_name, session=None, autocommit=True):
        s = self.build_session(session)

        room = self.get_or_create(room_name, session, False)

        player = None
        if not room.has_player(player_name):
            player = PlayerDAO.create_player(session=s, name=player_name, palitos=3)
            room.add_player(player)
            s.add(player)

            self.save(room, session, autocommit)

        else:
            player = room.get_player(name=player_name)

        return player

    def filter_get(self, query, room_name, *k, **kw):
        return query.filter(Room.name == room_name)

    def make_model(self, room_name, *k, **kw):
        return Room(name=room_name)
