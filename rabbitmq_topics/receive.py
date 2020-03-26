# -*- coding: utf-8 -*-
import pika
import sys

from rabbitmq_helper.rabbit_mq_base import RabbitMqLogin

mq = RabbitMqLogin()
connection = mq.rabbitMq_login()
channel = connection.channel()

channel.exchange_declare(exchange='topic_logs', exchange_type='topic')

result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

binding_keys = sys.argv[1:]
if not binding_keys:
    sys.stderr.write("Usage: %s [binding_key]...\n" % sys.argv[0])
    sys.exit()

for binding_key in binding_keys:
    channel.queue_bind(exchange='topic_logs', queue=queue_name, routing_key=binding_key)


def callback(ch, method, properties, body):
    print("{0}, {1}".format(method.routing_key, body))


channel.basic_consume(on_message_callback=callback, queue=queue_name, auto_ack=True)

channel.start_consuming()
