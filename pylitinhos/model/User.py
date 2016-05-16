from . import BaseModel

import sqlalchemy
from sqlalchemy import Column

class User(BaseModel):
    __tablename__ = 'users'

    id = Column(sqlalchemy.Integer(), primary_key=True)
    username = Column(sqlalchemy.String(150), unique=True)

    #Não faça isso em casa
    password = Column(sqlalchemy.String(100))
