import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask
from messages_service import MessageService


app = Flask(__name__)
message_service = MessageService(app)


@app.route('/msg', methods=['GET'])
def get_message():
    try:
        return message_service.get_message()
    except Exception as e:
        return message_service.handle_error(f'Error fetching message: {e}')
    

def main():
    assert len(sys.argv) > 1, "Unfortunatly, I don`t get any port number"
    app.run(host='0.0.0.0', port=int(sys.argv[-1]), debug=True)


if __name__ == '__main__':
    main()   