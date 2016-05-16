from .DbTestCase import DbTestCase
from sqlalchemy.exc import IntegrityError

class TestUserDAO(DbTestCase):
    USERNAME = 'fulano'
    PASSWORD = '123456'
    NICKNAME = 'fulaninho'

    def test_create(self):
        user = self.given_some_created_user()
        self.assertIsNotNone(user)
        self.assertIsNotNone(user.id)
        self.assertEqual(user.username, self.USERNAME)
        self.assertEqual(user.password, self.PASSWORD)
        self.assertEqual(user.nickname, self.NICKNAME)

        self.assertTrue(self.db.users.exist(user.username))

    def test_verify_login(self):
        user = self.given_some_created_user()

        self.assertTrue(self.db.users.verify(user.username, user.password))

    def test_create_duplicate_user(self):
        self.given_some_created_user()

        with self.assertRaises(IntegrityError):
            #Tenta criar usuario com mesmo nome
            self.db.users.create(self.USERNAME, 'outra senha', nickname='pelido')

    def given_some_created_user(self):
        return self.db.users.create(self.USERNAME, self.PASSWORD, nickname=self.NICKNAME);
