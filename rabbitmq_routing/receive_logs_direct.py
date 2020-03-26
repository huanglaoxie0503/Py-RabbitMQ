# -*- coding: utf-8 -*-
import pika
import sys

from rabbitmq_helper.rabbit_mq_base import RabbitMqLogin

mq = RabbitMqLogin()
connection = mq.rabbitMq_login()
channel = connection.channel()

# 创建一个交换机，类型为:direct 即订阅模式。和发送端保持一致
channel.exchange_declare(exchange='direct_logs', exchange_type='direct')

# 声明零时队列
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

severities = sys.argv[1:]
if not severities:
    sys.stderr.write("Usage: %s [info] [warning] [error]\n" % sys.argv[0])
    sys.exit(1)

"""
使用routing_key 绑定交换机和队列，广播类型无需使用这个
direct类型：会对消息进行精确匹配
"""

for severity in severities:
    channel.queue_bind(exchange='direct_logs', queue=queue_name, routing_key=severity)


def callback(ch, method, properties, body):
    print("{0}, {1}".format(method.routing_key, body))


channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()
