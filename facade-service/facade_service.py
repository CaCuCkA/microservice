import uuid
import random
import requests
from base import BaseService

class FacadeService(BaseService):
    def __init__(self, app):
        super().__init__(app)
        self.__messages_service_url = 'http://messages_service:5005'
        self.__logging_service_urls = ['http://logging_service_1:5001', 'http://logging_service_2:5002', 'http://logging_service_3:5003']


    @staticmethod    
    def __generate_uuid():
        return str(uuid.uuid4())
    

    @staticmethod
    def __concat_resonses(messages: str, message: str) -> str:
        return messages + "\n" + message    
    

    def __choose_logging_service_url(self) -> str:
        return random.choice(self.__logging_service_urls)
    

    def __generate_url(self, service_type: str, endpoint: str) -> str:
        if service_type == 'logging':
            url = self.__choose_logging_service_url()
            return f"{url}{endpoint}"
        elif service_type == 'message':
            return f"{self.__messages_service_url}{endpoint}"
        else:
            raise ValueError("Invalid service type")


    def __get_messages(self) -> str:
        url = self.__generate_url('logging', '/msgs')
        try:
            response = requests.get(url)
            response.raise_for_status()
            res = response.json()['msgs']
            return res
            
        except Exception as e:
            raise e


    def __get_static_message(self) -> str:
        url = self.__generate_url('message', '/msg')
        try:
            response = requests.get(url)
            response.raise_for_status()
            res = response.json()['msg']
            return res
            
        except Exception as e:
            raise e
        

    def send_message(self, data, app):
        uuid = self.__generate_uuid()
        url = self.__generate_url('logging', '/log')
        app.logger.info(f"URL: {url}, Message: {data.get('msg')}")

        try:
            response = requests.post(url, json={'id': uuid, 'msg': data.get('msg')})
            response.raise_for_status()
            return response.json(), 200
        
        except Exception as e:
            return self.handle_error(str(e))
    

    def get_data(self):
        try:
            messages = self.__get_messages()
            message = self.__get_static_message()
            result = self.__concat_resonses(messages, message)
            return self._generate_output(result=result)
        
        except Exception as e:
            return self.handle_error(str(e))
