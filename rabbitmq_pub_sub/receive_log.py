# -*- coding: utf-8 -*-
import pika

from rabbitmq_helper.rabbit_mq_base import RabbitMqLogin

"""
所有的接收端获取的所有的消息
"""

mq = RabbitMqLogin()
connection = mq.rabbitMq_login()
channel = connection.channel()

# 此处需要和发送端保持一致
channel.exchange_declare(exchange='logs', exchange_type='fanout')
# 需做个临时队列。消费端断开后就自动删除
result = channel.queue_declare(queue='', exclusive=True)
# 取得队列名称
queue_name = result.method.queue
# 将队列和交换机绑定一起
channel.queue_bind(exchange='logs', queue=queue_name)


def callback(ch, method, properties, body):
    print("receive:{0}".format(str(body, encoding='utf-8')))


channel.basic_consume(queue=queue_name, auto_ack=True, on_message_callback=callback)

channel.start_consuming()
