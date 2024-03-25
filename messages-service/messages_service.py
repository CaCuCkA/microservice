import logging
import threading
from base import client, BaseService

class MessagesService(BaseService):
    def __init__(self, app, port: int, id: int):
        self.__messages = []
        super().__init__(app, BaseService._camel_to_snake(__class__.__name__, id), port)
        self.__communication_queue = client.get_queue(self._consul_client.kv.get("queue_name")[1]['Value'].decode('utf-8')).blocking()
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
