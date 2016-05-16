
class Player(object):
    def __init__(self, **kw):
        self.name = kw.get('name', '')
        self.palitos = 0
