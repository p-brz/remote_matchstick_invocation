from . import DataSession
from .UserDAO import UserDAO
from .RoomDAO import *
from .PlayerDAO import *


class Data(object):

    def __init__(self, **kw):
        self.dbSession = DataSession(dbfile=kw.get('dbfile', DataSession.DEFAULT_DBFILE))
        self.dbSession.create()
        # self.usersDAO = UserDAO(self.dbSession.make_builder())
        self.users = UserDAO()
        self.rooms = RoomDAO()
        self.players = PlayerDAO()

    def destroy(self):
        self.dbSession.destroy()
