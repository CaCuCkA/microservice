import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, request
from facade_service import FacadeService

app = Flask(__name__)
facade_service = FacadeService()


@app.route('/msg', methods=['POST'])
def post_message():
    try:
        data = request.json
        return facade_service.send_message(data)
    except Exception as e:
        print(str(e))
        return facade_service.handle_error(f'Error handling get message request: {e}') 


@app.route('/msgs', methods=['GET'])
def get_msgs():
    try:
        return facade_service.get_data()
    except Exception as e:
        return  facade_service.handle_error(f'Error handling get message request: {e}') 


if __name__ == '__main__':
    app.run(port=5000)