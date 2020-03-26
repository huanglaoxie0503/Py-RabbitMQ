# -*- coding: utf-8 -*-
import sys
import pika
from rabbitmq_helper.rabbit_mq_base import RabbitMqLogin


mq = RabbitMqLogin()
connection = mq.rabbitMq_login()

channel = connection.channel()

# durable: 保证 server 挂了，队列依然存在
channel.queue_declare(queue='task_queue', durable=True)

msg = "".join(sys.argv[1:]) or "600519.SH"
# exchange为空，使用默认交换机，delivery_mode=2：使消息持久化，队列名称绑定routing_key
channel.basic_publish(exchange='', routing_key='task_queue', body=msg, properties=pika.BasicProperties(delivery_mode=2,))

print("Sent: {0}".format(msg))

connection.close()
