from .DataSession import SessionBuilder

class BaseDAO(object):
    # def __init__(self, session_builder):
    #     self.session_builder = session_builder
    def __init__(self):
        self.session_builder = SessionBuilder()

    def build_session(self, session=None):
        return self.session_builder.build_session(session)
