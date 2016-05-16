from . import DataSession
from .UserDAO import UserDAO
from .RoomDAO import *

class Data(object):
    def __init__(self, **kw):
        self.dbSession = DataSession(dbfile = kw.get('dbfile', None))
        self.dbSession.create()
        # self.usersDAO = UserDAO(self.dbSession.make_builder())
        self.users = UserDAO()
        self.rooms = RoomDAO()

    def destroy(self):
        self.dbSession.destroy()
