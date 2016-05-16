# -*- coding: utf-8 -*-
from pylitinhos.model.Room import *
from pylitinhos.model.Player import *


class Error(object):

    class Causes:
        PlayerAlreadyOnRoom = 1
        InvalidLogin = 2
        NewUser = 3

        msgs = {
            PlayerAlreadyOnRoom: "Jogador já foi adicionado a esta sala"
        }

        @staticmethod
        def get_msg(cause):
            return msgs.get(cause, 'Unknown')

    def __init__(self, cause):
        self.cause = cause


class Bundle(object):

    def __init__(self, data={}):
        self.data = data

    def add_data(self, data, value):
        self.data.update({data: value})

    def get_data(self, data):
        return self.data[data]


class Response(object):

    def __init__(self, **kw):
        self.error = kw.get('error', None)
        self.bundle = kw.get('bundle', None)

    def is_ok(self):
        return self.error is None

    @property
    def cause(self):
        if self.error:
            return self.error.cause

        return None

    @cause.setter
    def cause(self, cause):
        if not self.error:
            self.error = Error(cause)
        else:
            self.error.cause = cause

    def error_msg(self):
        if self.error:
            return Error.Causes.get_msg(self.error_cause())
        return None
