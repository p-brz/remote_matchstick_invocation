from .BaseModel import BaseModel

import sqlalchemy
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm.collections import attribute_mapped_collection

class Room(BaseModel):
    __tablename__ = "rooms"

    id = Column(sqlalchemy.Integer(), primary_key=True)
    name = Column(sqlalchemy.String(150), unique=True)
    players = relationship("Player", collection_class=attribute_mapped_collection('name'))

    def add_player(self, player):
        self.players[player.name] = player

    def has_player(self, player_name):
        return player_name in self.players

    def get_player(self, **kw):
        player_name = kw.get('name', None)

        return self.players.get(player_name, None)
