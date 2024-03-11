import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from logging_service import LoggingService
from flask import Flask, request


app = Flask(__name__)
logging_service = LoggingService(app)


@app.route('/log', methods=['POST'])
def log_message():
    try:
        data = request.json
        return logging_service.log_message(data)
    except Exception as e:
        return logging_service.handle_error(f'Error handling get message request: {request.json}') 


@app.route('/msgs', methods=['GET'])
def get_messages():
    try:
        return logging_service.get_message_values()
    except Exception as e:
        return logging_service.handle_error(f'Error handling get message request: {e}')


def main():
    assert len(sys.argv) > 1, "Unfortunatly, I don`t get any port number"
    app.run(host='0.0.0.0', port=int(sys.argv[-1]), debug=True)


if __name__ == '__main__':
    main()   