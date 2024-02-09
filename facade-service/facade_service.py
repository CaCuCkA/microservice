import uuid
import requests
from flask import jsonify
from base.base_service import BaseService


class FacadeService(BaseService):
    def __init__(self):
        super().__init__()
        self.__logging_service_url = 'http://localhost:5001'
        self.__messages_service_url = 'http://localhost:5002'


    @staticmethod    
    def __generate_uuid():
        return str(uuid.uuid4())
    

    @staticmethod
    def __concat_resonses(messages: str, message: str) -> str:
        return messages + "\n" + message    
    


    def __generate_url(self, service_type: str, response: str):
        return (self.__logging_service_url if service_type == 'logging' else self.__messages_service_url) + response


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
        

    def send_message(self, data):
        uuid = self.__generate_uuid()
        url = self.__generate_url('logging', '/log')

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
