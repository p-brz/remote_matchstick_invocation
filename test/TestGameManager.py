from .DbTestCase import DbTestCase
from unittest.mock import Mock

from pylitinhos.remote import GameManager

class TestGameManager(DbTestCase):
    USERNAME = 'fulano'
    PASSWORD = '123456'
    NICKNAME = 'fulaninho'
    ROOMNAME = 'sala X'

    def setUp(self):
        super(TestGameManager, self).setUp()

        self.game_manager = GameManager(db=self.db)
        self.game_manager.synchronous = True

    def test_register_player_to_room(self):
        self.assertFalse(self.db.users.exist(self.USERNAME))
        user = self.given_an_existent_user()

        res = self.game_manager.room_exist(self.ROOMNAME)

        self.assertTrue(res.is_ok())
        self.assertFalse(res.bundle.get_data('exist'))

        #Criar sala com jogador
        res = self.game_manager.add_player_to_room(user.username, self.ROOMNAME)
        self.assertTrue(res.is_ok())

        print(res.bundle.data)
        player = res.bundle.get_data('player')
        self.assertIsNotNone(player)
        self.assertEqual(player.name, user.username)

    def test_try_register_player_without_user(self):
        res = self.game_manager.add_player_to_room("inexistent user", self.ROOMNAME)

        self.assertFalse(res.is_ok())

    def test_get_room(self):
        room = self.given_a_room_with_some_users()
        room_name = room.name
        player_count = len(room.players)
        self.assertGreater(player_count, 1)

        self.game_manager.db = self.reset_db()
        res = self.game_manager.get_room(room_name)
        res_room = res.bundle.get_data('room')

        self.assertTrue(res.is_ok())
        self.assertIsNotNone(res_room)
        self.assertEqual(res_room.name, room_name)
        self.assertEqual(len(res_room.players), player_count)

    def test_make_guess(self):
        room = self.given_a_room_with_some_users()

        observer = Mock()
        self.game_manager.observe_room(room.name, observer)

        self.game_manager.setup_game(room.name)

        for pname in room.players:
            self.game_manager.room_infos[room.name]['bets'] = {
                    pname : 2
            }

        res = self.game_manager.make_guess(room.name, self.USERNAME, 4)

        self.assertTrue(res.is_ok())
        self.assertTrue(observer.on_event.called)


    def test_observe_room(self):
        room = self.db.rooms.create(self.ROOMNAME)

        #Adicionar observer
        mockObserver = Mock(spec=['on_event'])
        self.game_manager.observe_room(room.name, mockObserver)

        #Ao adicionar um novo jogador
        self.create_player_at_room(room.name, self.USERNAME)
        self.create_player_at_room(room.name, 'sicrano')

        #observador é chamado de forma asincrona, então destroi game_manager
        # para forçar que observers sejam chamados
        self.game_manager.destroy()

        #Então o observador deve ser chamado
        self.assertTrue(mockObserver.on_event.called)
        self.assertEqual(mockObserver.on_event.call_count, 2)

    def given_a_room_with_some_users(self):
        # u1 = self.given_an_existent_user()
        # u2 = self.given_an_existent_user(username='outro usuario', nickname='nick')

        # self.db.rooms.add_player(self.ROOMNAME, u1.username)
        # self.db.rooms.add_player(self.ROOMNAME, u2.username)

        self.create_player_at_room(self.ROOMNAME, 'algum usuario')
        self.create_player_at_room(self.ROOMNAME, 'outro', nickname='nick')

        return self.db.rooms.get(self.ROOMNAME)

    def given_an_existent_user(self, **kw):
        return self.create_user(**kw)

    def create_player_at_room(self, room_name, username, **kw):
        self.create_user(username=username, **kw)
        return self.game_manager.add_player_to_room(username, room_name)

    def create_user(self, **kw):
        return self.db.users.create(kw.get('username', self.USERNAME),
                                    kw.get('password', self.PASSWORD),
                                    nickname=kw.get('nickname', self.NICKNAME))
