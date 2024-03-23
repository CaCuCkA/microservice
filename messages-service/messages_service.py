from base import BaseService
from base import client

class MessageService(BaseService):
    def __init__(self, app):
        super().__init__(app)
        self.__messages = []
        self.__comunication_queue = client.get_queue("messages-queue").blocking()
    

    def get_message(self):
        return self._generate_output(msg='This is a static message from messages-service.')
