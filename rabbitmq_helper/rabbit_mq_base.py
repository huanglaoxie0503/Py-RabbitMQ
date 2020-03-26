# -*- coding: utf-8 -*-
import pika


class RabbitMqLogin(object):
    def __init__(self):
        self.host = '127.0.0.1'
        self.user = 'admin'
        self.password = 'admin'
        self.port = 5672
        self.queue = 'hello'

    def rabbitMq_login(self):
        # 添加RabbitMQ 用户名和密码
        credentials = pika.PlainCredentials(self.user, self.password)
        # 连接队列服务器
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host, port=self.port,
                                                                       credentials=credentials))

        return connection
