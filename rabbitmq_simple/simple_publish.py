# -*- coding: utf-8 -*-
import pika

# 添加RabbitMQ 用户名和密码
credentials = pika.PlainCredentials('admin', 'admin')
# 连接队列服务器
connection = pika.BlockingConnection(pika.ConnectionParameters(host="47.106.174.103", port=5672,
                                                               credentials=credentials))
# 创建队列。有就不管，没有就自动创建
channel = connection.channel()
# 使用默认的交换机发送消息。exchange为空就使用默认的
channel.queue_declare(queue="hello")

for i in range(10000):
    body = "I Love You -->{0}".format(i)
    channel.basic_publish(exchange="", routing_key="hello", body=body)

    print("Sent {0}".format(body))

connection.close()
