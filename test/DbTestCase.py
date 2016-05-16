import unittest
import os

from pylitinhos.db.Data import Data

class DbTestCase(unittest.TestCase):
    DB_FILE = '/tmp/dbfile.sqlite'

    def setUp(self):
        self.db = Data(dbfile = self.DB_FILE)

    def tearDown(self):
        self.db.destroy()
        os.remove(self.DB_FILE)
