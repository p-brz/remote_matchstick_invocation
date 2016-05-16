from .BaseModel import BaseModel

import sqlalchemy
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship, backref

from .User import User

class Player(BaseModel):
    __tablename__ = "players"
    id = Column(sqlalchemy.Integer, primary_key=True)
    user_id = Column(sqlalchemy.Integer, ForeignKey(User.__tablename__ + ".id"))
    user = relationship("User", backref=backref(__tablename__, uselist=False))

    room_id = Column(sqlalchemy.Integer, ForeignKey('rooms.id'))

    palitos = Column(sqlalchemy.Integer)

    def __init__(self, **kw):
        kw['palitos'] = kw.get('palitos', 0)
        super(Player, self).__init__(**kw)

    def _get_user(self):
        if self.user is None:
            self.user = User()

        return self.user

    @property
    def name(self):
        return self._get_user().username

    @name.setter
    def name(self, value):
        self._get_user().username = value
