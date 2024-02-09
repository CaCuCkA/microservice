from base.base_service import BaseService

class LoggingService(BaseService):
    def __init__(self):
        super().__init__()
        self.__messages_log = {}

    def log_message(self, data) -> dict:
        message_id, message = self._message_parser(data, ['id', 'msg'])
        self.__messages_log[message_id] = message
        self._logger(message)
        return self._generate_output(id=message_id)
    
    
    def get_message_values(self):
        messages = list(self.__messages_log.values())
        return self._generate_output(msgs=' '.join(messages) if messages else '')

