from hazelcast.config import Config
from hazelcast import HazelcastClient as HzClient 


def singleton(cls):
    instances = {}
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance


@singleton
class HazelcastClient:
    def __init__(self) -> None:
        self.__client = self.__setup_client()

    @property
    def client(self):
        return self.__client

    def __setup_client(self) -> HzClient:
        config = Config()
        config.cluster_name = "hazelcast-homework2"
        config.cluster_members = [
            "hazelcast-node1:5701",
            "hazelcast-node2:5701",
            "hazelcast-node3:5701"
        ]

        return HzClient(config)


client = HazelcastClient().client