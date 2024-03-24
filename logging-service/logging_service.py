import logging
from base import client
from base import BaseService


class LoggingService(BaseService):
    def __init__(self, app):
        super().__init__(app)        
        self.__messages_log = client.get_map("messages-map").blocking() 


    def log_message(self, data) -> dict:
        logging.info(f"Accept message: {data.get('msg')}")
        message_id, message = self._message_parser(data, ["id", "msg"])
        self.__messages_log.put(message_id, message)
        return self._generate_output(id=message_id)
    
    
    def get_message_values(self):
        messages = self.__messages_log.values()
        return self._generate_output(msgs=" ".join(messages) if messages else "")
