import unittest
import os

from pylitinhos.db.Data import Data

class TestUserDAO(unittest.TestCase):
    DB_FILE = '/tmp/dbfile.sqlite'

    def setUp(self):
        self.db = Data(dbfile = self.DB_FILE)

    def tearDown(self):
        self.db.destroy()
        os.remove(self.DB_FILE)

    def test_create(self):
        user = self.given_some_created_user()
        self.assertIsNotNone(user)
        self.assertTrue(self.db.users().exist(user.username))

    def test_verify_login(self):
        user = self.given_some_created_user()

        self.assertTrue(self.db.users().verify(user.username, user.password))

    def given_some_created_user(self):
        return self.db.users().create('fulano', '123456');
