import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask
from messages_service import MessageService


app = Flask(__name__)
message_service = MessageService(app)


@app.route('/msgs', methods=['GET'])
def get_messages():
    return message_service.get_messages()


def main():
    assert len(sys.argv) > 1, "Unfortunatly, I don`t get any port number"
    app.run(host='0.0.0.0', port=int(sys.argv[-1]))
    

if __name__ == '__main__':
    main()   