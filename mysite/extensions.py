class Notification(object):
    def __init__(self, name="", message="", level="info"):
        self.name = name
        self.message = message
        self.level = level

class Message(object):

    CLEAR_TABLE_MODEL = "cleartablemodel"

    @staticmethod
    def new_message(request, action, parameter):
        msg = SessionMessage(action, parameter)
        return msg

    def __init__(self, action, parameter):
        self.action = action
        self.parameter = parameter
