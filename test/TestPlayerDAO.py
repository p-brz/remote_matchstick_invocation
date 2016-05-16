from .DbTestCase import DbTestCase

from pylitinhos.model import *
from pylitinhos.db.PlayerDAO import PlayerDAO


class TestPlayerDAO(DbTestCase):
    ROOM_NAME = 'testroom'
    USERNAME = 'testuser'
    PASSWORD = '123456'

    def test_update(self):
        player = self.given_a_existent_player()
        player.palitos = 3
        player_id = player.id
        self.db.players.save(player)

        self.db.destroy()
        self.db = self.create_db()

        player = self.db.players.get(id=player_id)
        self.assertEqual(player.palitos, 3)

    def build_session(self, session=None):
        return self.db.players.build_session(session)

    def given_a_existent_player(self, session=None):
        s = self.build_session(session)
        user = self.given_some_user(s)
        player = PlayerDAO.create_player(session=s, name=user.username)
        self.db.players.save(player, s)

        return player

    def given_some_user(self, session=None):
        return self.db.users.create(self.USERNAME, self.PASSWORD, session)
