 # -*- coding: utf-8 -*-
from pylitinhos.model.Room import *
from pylitinhos.model.Player import *

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

    def error_cause(self):
        if self.error:
            return self.error.cause

        return None

    def error_msg(self):
        if self.error:
            return Error.Causes.get_msg(self.error_cause())
        return None
