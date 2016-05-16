from .DataSession import SessionBuilder

class BaseDAO(object):
    # def __init__(self, session_builder):
    #     self.session_builder = session_builder
    def __init__(self, ModelClass=None):
        self.session_builder = SessionBuilder()
        self.ModelClass = ModelClass

    def build_session(self, session=None, **kw):
        return self.session_builder.build_session(kw.get('session', session))

    def exist(self, *k, **kw):
        return self.get(*k, **kw) is not None

    def get(self, *k, **kw):
        s = self.build_session(**kw)

        q = s.query(self.ModelClass)
        return self.filter_get(q, *k, **kw).one_or_none()

    def create(self, *k, **kw):
        s = self.build_session(**kw)
        entity = self.make_model(*k, **kw)

        s.add(entity)

        if(kw.get('autocommit', True)):
            s.commit()

        return entity

    def filter_get(self, query, *k, **kw):
        raise NotImplementedError()

    def make_model(self, *k, **kw):
        raise NotImplementedError()
