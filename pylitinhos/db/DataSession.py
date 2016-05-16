import sqlalchemy
from pylitinhos import model
from sqlalchemy.engine import Engine
from sqlalchemy import event


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    '''
    Enable foreign keys check on sqlite.
    @See http://stackoverflow.com/questions/
         2614984/sqlite-sqlalchemy-how-to-enforce-foreign-keys
    '''
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


class DataSession(object):
    from sqlalchemy.orm import sessionmaker
    Session = sqlalchemy.orm.scoping.scoped_session(sessionmaker())

    def __init__(self, **kwargs):
        self.dbfile = kwargs.get('dbfile', '.data.sqlite')

        from sqlalchemy import create_engine
        engine = 'sqlite:///' + self.dbfile
        self.engine = create_engine(engine,
                                    connect_args={'check_same_thread': False})

        DataSession.Session.configure(bind=self.engine)

    def create(self):
        model.BaseModel.metadata.create_all(self.engine)

    def destroy(self):
        DataSession.Session.remove()
    # def make_builder(self):
    #     return SessionBuilder(self.engine)


class SessionBuilder(object):
    # def __init__(self, engine):
    #     self.engine = engine

    def build_session(self, dbSession=None):
        # return dbSession if dbSession is not None else
        # DataSession.Session(bind=self.engine)
        return dbSession if dbSession is not None else DataSession.Session()
