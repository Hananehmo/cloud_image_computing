import hashlib
import boto3
from werkzeug.utils import secure_filename

import s3
import db_client
import rabbitmq
from flask import request, Flask

app = Flask(__name__)


def generate_hash(id):
    hash_object = hashlib.md5(id.encode())
    hash_code = hash_object.hexdigest()
    return hash_code


@app.route('/user', methods=['POST'])
def get_info():
    name = request.form.get('name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')
    id = request.form.get('id')
    hash_id = generate_hash(id)
    ip = request.remote_addr
    image = request.files['image']
    filename = secure_filename(id + '.jpg')
    folder_path = 'H:\\cloud\\Tamrin 1\\image_upload'
    image.save(folder_path + '/' + filename)
    print("file saved successfully")
    db_client.write_to_mongodb({
        'name': name,
        'last_name': last_name,
        'email': email,
        'id': id,
        'hash_id': hash_id,
        'ip': ip
    })
    rabbitmq.add_id(id)
    s3.s3_upload(id)
    return 'Ok'


if __name__ == '__main__':
    app.run(port=7777)
