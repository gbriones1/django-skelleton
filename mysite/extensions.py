class Notification(object):
    def __init__(self, name, message):
        self.name = name
        self.message = message

class NotificationHandler(object):

    QUEUE = []

    @staticmethod
    def add_notification(name, message):
        NotificationHandler.QUEUE.append(Notification(name, message))

    @staticmethod
    def remove_notification(name):
        new_queue = []
        for n in NotificationHandler.QUEUE:
            if n.name != name:
                new_queue.append(n)
        NotificationHandler.QUEUE = new_queue
