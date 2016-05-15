from . import DataSession
from .UserDAO import UserDAO

class Data(object):
    def __init__(self, **kw):
        self.dbSession = DataSession(dbfile = kw.get('dbfile', None))
        self.dbSession.create()
        # self.usersDAO = UserDAO(self.dbSession.make_builder())
        self.usersDAO = UserDAO()

    def destroy(self):
        self.dbSession.destroy()

    def users(self):
        return self.usersDAO
