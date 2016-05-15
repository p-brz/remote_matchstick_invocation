from . import BaseModel

import sqlalchemy
from sqlalchemy import Column

class User(BaseModel):
    __tablename__ = 'users'

    username = Column(sqlalchemy.String(150), primary_key=True)

    #Não faça isso em casa
    password = Column(sqlalchemy.String(100))
