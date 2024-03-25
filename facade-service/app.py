import os
import sys
import logging

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from facade_service import FacadeService
from base import BaseService
from flask import Flask, request, jsonify


app = Flask(__name__)
facade_service = None
BaseService.setup_logging()


@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200


@app.route('/msg', methods=['POST'])
def post_message():
    try:
        data = request.json
        return facade_service.send_message(data)
    except Exception as e:
        return facade_service.handle_error(f'Error handling get message request: {e}') 


@app.route('/msgs', methods=['GET'])
def get_msgs():
    try:
        return facade_service.get_data()
    except Exception as e:
        return  facade_service.handle_error(f'Error handling get message request: {e}') 


def main():
    global facade_service
    assert len(sys.argv) > 1, "Unfortunatly, I don`t get any port number"
    port = int(sys.argv[-1])
    facade_service = FacadeService(app, port)
    app.run(host='0.0.0.0', port=port, debug=True)


if __name__ == '__main__':
    main()

