from base.base_service import BaseService


class MessageService(BaseService):
    def __init__(self, app):
        super().__init__(app)
    

    def get_message(self):
        return self._generate_output(msg='This is a static message from messages-service.')
