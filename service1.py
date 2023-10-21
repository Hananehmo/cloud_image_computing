import base64
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
    hash_code = hash_object.digest()
    base64_code = base64.b64encode(hash_code).decode('utf-8')
    return base64_code


@app.route('/user', methods=['POST'])
def get_info():
    name = request.form.get('name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')
    id = request.form.get('id')
    hash_id = generate_hash(id)
    ip = request.remote_addr
    image1 = request.files['image1']
    filename1 = secure_filename(id + '_1.jpg')
    folder_path = 'image_upload'
    image1.save(folder_path + '/' + filename1)
    image2 = request.files['image2']
    filename2 = secure_filename(id + '_2.jpg')
    image2.save(folder_path + '/' + filename2)
    print("file saved successfully")
    db_client.write_to_mongodb({
        'name': name,
        'last_name': last_name,
        'email': email,
        'hash_id': hash_id,
        'ip': ip,
        'state': 'pending'
    })
    rabbitmq.add_id(id)
    s3.s3_upload(id)
    print('file uploaded successfully!')
    # s3.s3_download(id)
    return 'Ok'


@app.route('/get-status', methods=['POST'])
def get_status():
    id = request.form.get('id')
    ip = request.remote_addr
    base64_id = generate_hash(id)
    client = db_client.read_from_mongodb({'hash_id': base64_id, 'ip': ip})
    return client['state']


if __name__ == '__main__':
    app.run(port=7777)
