import base64
import hashlib

import pika
import json
import s3
import imagga
import mailgun
import db_client


def generate_hash(id):
    hash_object = hashlib.md5(id.encode())
    hash_code = hash_object.digest()
    base64_code = base64.b64encode(hash_code).decode('utf-8')
    return base64_code


def success(id):
    base64_id = generate_hash(id)
    client = db_client.read_from_mongodb({'hash_id': base64_id})
    print(client)
    db_client.update_mongodb(base64_id, 'success')
    mailgun.send_email(client['email'], 'success')


def failed(id):
    base64_id = generate_hash(id)
    client = db_client.read_from_mongodb({'hash_id': base64_id})
    db_client.update_mongodb(base64_id, 'failed')
    mailgun.send_email(client['email'], 'failed')


def add_id(id):
    parameters = pika.URLParameters("amqps://acjqnrgz:FO_KG7JaGwGmMw0n8ttjbShcclOR5tDb@puffin.rmq2.cloudamqp.com/acjqnrgz")
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    channel.queue_declare(queue='hana')

    channel.basic_publish(exchange='', routing_key='hana', body=id)

    connection.close()


def retrieve_id():
    # Establish a connection to RabbitMQ
    parameters = pika.URLParameters("amqps://acjqnrgz:FO_KG7JaGwGmMw0n8ttjbShcclOR5tDb@puffin.rmq2.cloudamqp.com/acjqnrgz")
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    # Declare a queue
    channel.queue_declare(queue='hana')

    # Define a callback function to process incoming messages
    def callback(ch, method, properties, body):
        user = json.loads(body)
        # Process the user data
        print(user)

    # Start consuming messages
    channel.basic_consume(queue='hana', on_message_callback=callback, auto_ack=True)
    channel.start_consuming()


def listen_rabbitmq():
    # Establish a connection to RabbitMQ
    parameters = pika.URLParameters("amqps://acjqnrgz:FO_KG7JaGwGmMw0n8ttjbShcclOR5tDb@puffin.rmq2.cloudamqp.com/acjqnrgz")
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    # Declare a queue
    channel.queue_declare(queue='hana')

    # Define a callback function to process incoming messages
    def callback(ch, method, properties, body):
        # Process the message body
        data = body.decode('utf-8')
        print(f"Received message: {data}")
        s3.s3_download(data)
        face_id_1 = imagga.detection_face('image_downloaded\\' + data + '_1.jpg')
        face_id_2 = imagga.detection_face('image_downloaded\\' + data + '_2.jpg')
        score = imagga.check_similarity(face_id_1, face_id_2)
        if score > 80:
            success(data)
        else:
            failed(data)

    # Start consuming messages from the queue
    channel.basic_consume(queue='hana', on_message_callback=callback, auto_ack=True)

    # Keep the consumer running
    channel.start_consuming()
