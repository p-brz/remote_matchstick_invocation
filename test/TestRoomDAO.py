from .DbTestCase import DbTestCase

class TestRoomDAO(DbTestCase):
    ROOM_NAME = 'testroom'

    def test_get_or_create(self):
        room = self.db.rooms.get_or_create(self.ROOM_NAME)

        self.assertIsNotNone(room)
        self.assertIsNotNone(room.id)

        same_room = self.db.rooms.get_or_create(self.ROOM_NAME)

        self.assertEqual(room, same_room)
