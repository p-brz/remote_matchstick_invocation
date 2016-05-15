from . import BaseDAO
from pylitinhos.model.User import User

class UserDAO(BaseDAO):
    #
    # def __init__(self, session_builder):
    #     super(UserDAO, self).__init__(session_builder)

    def exist(self, username, session=None):
        return self.get(username, session) is not None

    def get(self, username, dbSession=None):
        s = self.build_session(dbSession)

        return s.query(User).filter(
            User.username == username).one_or_none()

    def create(self, username, password, session=None, autocommit=True):
        s = self.build_session(session)
        u = User(username=username, password=password)

        s.add(u)

        if(autocommit):
            s.commit()

        return u

    def verify(self, username, password):
        u = self.get(username)
        return u is not None and u.password == password
