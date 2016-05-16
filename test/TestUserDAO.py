from .DbTestCase import DbTestCase

class TestUserDAO(DbTestCase):

    def test_create(self):
        user = self.given_some_created_user()
        self.assertIsNotNone(user)
        self.assertIsNotNone(user.id)
        self.assertTrue(self.db.users.exist(user.username))

    def test_verify_login(self):
        user = self.given_some_created_user()

        self.assertTrue(self.db.users.verify(user.username, user.password))

    def given_some_created_user(self):
        return self.db.users.create('fulano', '123456');
