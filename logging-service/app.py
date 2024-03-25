import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from base import BaseService
from flask import Flask, request, jsonify
from logging_service import LoggingService

app = Flask(__name__)
logging_service = None
BaseService.setup_logging()


@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200


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
    global logging_service
    assert len(sys.argv) > 2, "Unfortunatly, I don`t get any port number"
    _, port, id = sys.argv
    logging_service = LoggingService(app, int(port), int(id))
    app.run(host='0.0.0.0', port=int(port), debug=True)


if __name__ == '__main__':
    main()   