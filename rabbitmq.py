import pika


def add_id(id):
    parameters = pika.URLParameters("amqps://acjqnrgz:FO_KG7JaGwGmMw0n8ttjbShcclOR5tDb@puffin.rmq2.cloudamqp.com/acjqnrgz")
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    channel.queue_declare(queue='hana')

    channel.basic_publish(exchange='', routing_key='hana', body=id)

    connection.close()
