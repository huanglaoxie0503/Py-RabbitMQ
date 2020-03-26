# -*- coding: utf-8 -*-
import pika

from rabbitmq_helper.rabbit_mq_base import RabbitMqLogin

mq = RabbitMqLogin()
connection = mq.rabbitMq_login()
channel = connection.channel()

"""
原则上消息只能由交换机到队列，有多个设备连接到交换机，此时交换机把消息发送给那个设备呢？发送依据就是根据交换机的类型来定。
交换机类型有：
    direct
    topic
    headers
    fanout：广播，即所有设备都能接收到消息。
"""
# 此处定义一个名为logs的fanout类型的交换机（exchange）
channel.exchange_declare(exchange='logs', exchange_type='fanout')

msg = "rabbitMq"

# 将消息发送到名为logs 的exchange中，因为交换机是fanout 类型，所以无需指定routing_key
channel.basic_publish(exchange='logs', routing_key='', body=msg)

print("Sent :{0}".format(msg))

connection.close()
