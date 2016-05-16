from .BaseModel import BaseModel

import sqlalchemy
from sqlalchemy import Column


class Room(BaseModel):
    __tablename__ = "rooms"

    id = Column(sqlalchemy.Integer(), primary_key=True)
    name = Column(sqlalchemy.String(150), unique=True)

    def __init__(self, **kw):
        super(Room, self).__init__(**kw)

        self.players = {}

    def add_player(self, player):
        self.players[player.name] = player

    def has_player(self, player_name):
        return player_name in self.players
