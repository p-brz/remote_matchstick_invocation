from .BaseDAO import BaseDAO
from pylitinhos.model.Player import Player
from pylitinhos.model.User import User

class PlayerDAO(BaseDAO):
    def __init__(self):
        super(PlayerDAO, self).__init__(Player)

    def filter_get(self, query, name=None, *k, **kw):
        id = kw.get('id', None)
        if id is not None:
            return query.filter(Player.id == id)

        return query.filter(Player.name == name)

    def make_model(self, *k, **kw):
        session = kw.get('session', None)
        name = kw.get('name', None)
        if session is not None and name is not None:
            return PlayerDAO.create_player(session, name)

        return Player(user_id=kw.get('user_id', None), user=kw.get('user', None))

    @staticmethod
    def create_player(session, name, palitos=0):
        user = session.query(User).filter(User.username == name).one()
        return Player(user_id = user.id, user = user, palitos=palitos)
