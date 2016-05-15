 # -*- coding: utf-8 -*-

class Player(object):
    def __init__(self, **kw):
        self.name = kw.get('name', '')
        self.palitos = 0

class Room(object):
    def __init__(self, **kw):
        self.name = kw.get('name', '')
        self.players = {}

    def add_player(self, player):
        self.players[player.name] = player

    def has_player(self, player_name):
        return player_name in self.players

class Error(object):
    class Causes:
        PlayerAlreadyOnRoom = 1

        msgs = {
            PlayerAlreadyOnRoom : "Jogador já foi adicionado a esta sala"
        }

        @staticmethod
        def get_msg(cause):
            return msgs.get(cause, 'Unknown')

    def __init__(self, cause):
        self.cause = cause

class Response(object):
    def __init__(self, **kw):
        self.error = kw.get('error', None)

    def is_ok(self):
        return self.error is None;
