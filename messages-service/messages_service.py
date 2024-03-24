import logging
import threading
from base import client, BaseService

class MessageService(BaseService):
    def __init__(self, app):
        super().__init__(app)
        self.__messages = []
        self.__communication_queue = client.get_queue("messages-queue").blocking()
        threading.Thread(target=self.poll_queue, daemon=True).start()


    def poll_queue(self):
        while True:
            message = self.__communication_queue.take()
            logging.info(f"Get message from queue: {message}")
            self.__messages.append(message)
                

    def get_messages(self):
        msgs = ", ".join(str(msg) for msg in self.__messages)
        self._app.logger.info(self.__messages)
        return self._generate_output(msgs=msgs)
