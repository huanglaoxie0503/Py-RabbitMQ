# -*- coding: utf-8 -*-
import pika
import sys

from rabbitmq_helper.rabbit_mq_base import RabbitMqLogin

mq = RabbitMqLogin()
connection = mq.rabbitMq_login()
channel = connection.channel()

channel.exchange_declare(exchange='topic_logs', exchange_type='topic')

routing_key = sys.argv[1] if len(sys.argv) > 2 else 'anonymous.info'

msg = "创建交换机和上一章一样"

channel.basic_publish(exchange='topic_logs', routing_key=routing_key, body=msg)

print("{0}, {1}".format(routing_key, msg))

connection.close()