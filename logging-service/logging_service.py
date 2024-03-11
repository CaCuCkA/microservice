from hazelcast.config import Config
from hazelcast import HazelcastClient
from base.base_service import BaseService


class LoggingService(BaseService):
    def __init__(self, app):
        super().__init__(app)        
        self.__client =  LoggingService.__setup_client()
        self.__messages_log = self.__client.get_map("messages").blocking()
    

    @staticmethod
    def __setup_client() -> HazelcastClient:
        config = Config()
        config.cluster_name = "hazelcast-homework2"
        config.cluster_members = [
            "hazelcast-node1:5701",
            "hazelcast-node2:5701",
            "hazelcast-node3:5701"
        ]

        return HazelcastClient(config)


    def log_message(self, data) -> dict:
        message_id, message = self._message_parser(data, ['id', 'msg'])
        self.__messages_log.put(message_id, message)
        self._logger(message)
        return self._generate_output(id=message_id)
    
    
    def get_message_values(self):
        messages = self.__messages_log.values()
        return self._generate_output(msgs=' '.join(messages) if messages else '')
