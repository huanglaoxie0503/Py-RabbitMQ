# -*- coding: utf-8 -*-
import pika
import time

from rabbitmq_helper.rabbit_mq_base import RabbitMqLogin

""" 将同一个消息发给多个客户端，即发布订阅模式"""

mq = RabbitMqLogin()
connection = mq.rabbitMq_login()
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)


def callback(ch, method, properties, body):
    print("Receive: {0}".format(body))
    time.sleep(body.count(b'.'))
    print("Done")

    ch.basic_ack(delivery_tag=method.delivery_tag)


"""
目前已经知道如何保证消息不丢失，可是有的消费快，有的消费慢，这样分发消息，有的累死而有的没事干，这个问题如何解决呢？
rabbitMq 已经考虑到了，谁干完了，通知 server， server 就派遣任务给谁。这样可以保证公平派遣。
那如何实现公平派遣呢？只需在 channel.basic_consume(queue='task_queue', on_message_callback=callback) 代码前加：
channel.basic_qos(prefetch_count=1)
"""
channel.basic_qos(prefetch_count=1)

channel.basic_consume(queue='task_queue', on_message_callback=callback)
channel.start_consuming()
