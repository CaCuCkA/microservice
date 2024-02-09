import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask
from messages_service import MessageService


app = Flask(__name__)
message_service = MessageService()


@app.route('/msg', methods=['GET'])
def get_message():
    try:
        return message_service.get_message()
    except Exception as e:
        return message_service.handle_error(f'Error fetching message: {e}')
    

if __name__ == '__main__':
    app.run(port=5002)