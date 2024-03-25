import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from base import BaseService
from flask import Flask, jsonify
from messages_service import MessagesService


app = Flask(__name__)
message_service = None
BaseService.setup_logging()


@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200


@app.route('/msgs', methods=['GET'])
def get_messages():
    return message_service.get_messages()


def main():
    global message_service
    assert len(sys.argv) > 2, "Unfortunatly, I don`t get any port number"
    _, port, id = sys.argv
    message_service = MessagesService(app, int(port), int(id))
    app.run(host='0.0.0.0', port=int(port))
    

if __name__ == '__main__':
    main()   