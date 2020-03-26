# -*- coding: utf-8 -*-
import pika

# 添加RabbitMQ 用户名和密码
credentials = pika.PlainCredentials('admin', 'admin')
# 连接队列服务器
connection = pika.BlockingConnection(pika.ConnectionParameters(host="47.106.174.103", port=5672,
                                                               credentials=credentials))
channel = connection.channel()
# 目的是为了保证队列一定存在
channel.queue_declare(queue="hello")


# 收到消息后的回调
def callback(ch, method, properties, body):
    print(" Received %r" % body)


channel.basic_consume('hello', auto_ack=True, on_message_callback=callback)
print(' [*] Waiting for messages. To exit press CTRL+C')

channel.start_consuming()