
class EventTypes(object):
    Shutdown    = 0
    AddedUser   = 1
    UserInput   = 2
    NewGame     = 3

    _str = {
        Shutdown : "Shutdown",
        AddedUser : "AddedUser",
        NewGame : "NewGame"
    }

    @staticmethod
    def to_str(type):
        return EventTypes._str.get(type, "Unknown")

class Event(object):
    def __init__(self, type, data=None, **kw):
        self.type = type
        self.data = data if data is not None else kw

    def __str__(self):
        return "{ type: %s; data: %s }" % (EventTypes.to_str(self.type), str(self.data))
