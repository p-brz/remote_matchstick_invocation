from .DbTestCase import DbTestCase

from pylitinhos.model import *

class TestRoomDAO(DbTestCase):
    ROOM_NAME = 'testroom'
    USERNAME = 'testuser'
    PASSWORD = '123456'

    def test_get_or_create(self):
        room = self.db.rooms.get_or_create(self.ROOM_NAME)

        self.assertIsNotNone(room)
        self.assertIsNotNone(room.id)

        same_room = self.db.rooms.get_or_create(self.ROOM_NAME)

        self.assertEqual(room, same_room)

    def test_add_player(self):

        room = self.given_some_room()
        user = self.given_some_user()

        session = self.db.rooms.build_session()

        #Ao adicionar um jogador a esta sala
        player = self.db.rooms.add_player(room.name, user.username)
        self.assertIsNotNone(player)

        #Destroy sessao para garantir que objeto seja recriado do banco
        self.db.destroy()
        self.db = self.create_db()

        #Ele deve ser persistido no banco de dados
        same_room = self.db.rooms.get(self.ROOM_NAME)

        self.assertIsNotNone(same_room.players)

        same_player = same_room.get_player(name=self.USERNAME)

        self.assertFalse(same_room is room)
        self.assertIsNotNone(same_player)
        self.assertIsNotNone(same_player.id)
        self.assertGreaterEqual(same_player.id, 0)

        #Jogador deve iniciar com 3 palitos
        self.assertEqual(same_player.palitos, 3)

    def given_some_room(self, session=None):
        return self.db.rooms.create(self.ROOM_NAME, session)

    def given_some_user(self, session=None):
        return self.db.users.create(self.USERNAME, self.PASSWORD, session)
