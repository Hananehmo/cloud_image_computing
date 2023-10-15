import hashlib
import db_client
from flask import request, jsonify, Flask
import socket

app = Flask(__name__)


def generate_hash(id):
    hash_object = hashlib.md5(id.encode())
    hash_code = hash_object.hexdigest()
    return hash_code


@app.route('/user', methods=['POST'])
def get_info():
    data = request.get_json()
    name = data.get('name')
    last_name = data.get('last_name')
    email = data.get('email')
    id = data.get('id')
    hash_id = generate_hash(id)
    ip = request.remote_addr

    db_client.write_to_mongodb(data)
    return 'Ok'


if __name__ == '__main__':
    app.run(port=7777)
