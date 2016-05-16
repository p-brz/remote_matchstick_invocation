from .DbTestCase import DbTestCase

from pylitinhos.remote import GameManager

class TestGameManager(DbTestCase):
    USERNAME = 'fulano'
    PASSWORD = '123456'
    NICKNAME = 'fulaninho'
    ROOMNAME = 'sala X'

    def setUp(self):
        super(TestGameManager, self).setUp()

        self.game_manager = GameManager(db=self.db)

    def test_register_player_to_room(self):
        self.assertFalse(self.db.users.exist(self.USERNAME))
        user = self.given_an_existent_user()

        res = self.game_manager.room_exist(self.ROOMNAME)

        self.assertTrue(res.is_ok())
        self.assertFalse(res.bundle.get_data('exist'))

        #Criar sala com jogador
        res = self.game_manager.add_player_to_room(user.username, self.ROOMNAME)
        self.assertTrue(res.is_ok())

        player = res.bundle.get_data('player')
        self.assertIsNotNone(player)
        self.assertEqual(player.name, user.username)

    def given_an_existent_user(self):
        return self.db.users.create(self.USERNAME, self.PASSWORD, nickname=self.NICKNAME)
