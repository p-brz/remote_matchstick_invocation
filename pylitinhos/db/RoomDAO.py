from .BaseDAO import BaseDAO
from pylitinhos.model.Room import Room

class RoomDAO(BaseDAO):
    def __init__(self):
        super(RoomDAO, self).__init__(Room)

    def get_or_create(self, room_name, session=None, autocommit=True):
        s = self.build_session(session)
        room = self.get(room_name, s)
        if room is None:
            room = self.create(room_name, session, autocommit)

        return room

    def filter_get(self, query, room_name, *k, **kw):
        return query.filter(Room.name == room_name)

    def make_model(self, room_name, *k, **kw):
        return Room(name=room_name)
