import uuid
import random
import typing
import logging
import requests
from base import client
from base import BaseService


class FacadeService(BaseService):
    def __init__(self, app, port: int):
        super().__init__(app, BaseService._camel_to_snake(__class__.__name__), port)
        self.__communication_queue = client.get_queue(self._consul_client.kv.get("queue_name")[1]['Value'].decode('utf-8')).blocking()


    @staticmethod    
    def __generate_uuid():
        return str(uuid.uuid4())
    

    @staticmethod
    def __concat_resonses(messages: str, message: str) -> str:
        return messages + "\n" + message    
    
    
    def __get_services_ip(self, service_name: str) -> typing.List[str]:
        services = self._consul_client.agent.services()
        logging.info(f"Services: {services}")
        return [service_info['Address'] for _, service_info in services.items() if service_info['Service'] == service_name]
            

    def __choose_service_url(self, service_name: str) -> str:
        res = self.__get_services_ip(service_name)
        self._app.logger.info(res)
        return random.choice(res)
    

    def __generate_url(self, service_name: str, endpoint: str) -> str:
        url = self.__choose_service_url(service_name)
        return f"{url}{endpoint}"


    def __get_logging_messages(self) -> str:
        url = self.__generate_url('logging_service', '/msgs')
        try:
            response = requests.get(url)
            response.raise_for_status()
            res = response.json()['msgs']
            return res
            
        except Exception as e:
            raise e


    def __get_messages(self) -> str:
        url = self.__generate_url('messages_service', '/msgs')
        try:
            response = requests.get(url)
            response.raise_for_status()
            res = response.json()['msgs']
            return res
            
        except Exception as e:
            raise e
        

    def send_message(self, data):
        uuid = self.__generate_uuid()
        url = self.__generate_url('logging_service', '/log')
       
        try:
            self.__communication_queue.put(data.get('msg'))
            response = requests.post(url, json={'id': uuid, 'msg': data.get('msg')})
            response.raise_for_status()
            return response.json(), 200
        
        except Exception as e:
            return self.handle_error(str(e))
    

    def get_data(self):
        try:
            messages = self.__get_logging_messages()
            message = self.__get_messages()
            result = self.__concat_resonses(messages, message)
            return self._generate_output(result=result)
        
        except Exception as e:
            return self.handle_error(str(e))

