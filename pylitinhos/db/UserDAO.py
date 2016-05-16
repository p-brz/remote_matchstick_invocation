import hashlib
from pylitinhos.model.User import User
from . import BaseDAO


class UserDAO(BaseDAO):

    def __init__(self):
        super(UserDAO, self).__init__(User)

    def filter_get(self, query, username, *k, **kw):
        return query.filter(User.username == username)

    def make_model(self, username, password, *k, **kw):
        return User(username=username, password=password, **kw)

    def verify(self, username, password):
        u = self.get(username)
        return u is not None and u.password == password
