
from cli.smlite import SmLite
from .states import *


class PlayerInfo(object):
    pass


class Client(object):

    def __init__(self):
        self.player = PlayerInfo()
        self.sm = SmLite()
        self.sm.add_state('init', InitState(self.player))

    def start(self):
        self.sm.start('init')
