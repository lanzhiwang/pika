# -*- coding: utf-8 -*-
# pylint: disable=C0111,C0103,R0205

import logging
import pika
from pika import DeliveryMode
from pika.exchange_type import ExchangeType

logging.basicConfig(level=logging.DEBUG)

# class pika.credentials.PlainCredentials(username, password, erase_on_connect=False)
credentials = pika.PlainCredentials('guest', 'guest')

# class pika.connection.ConnectionParameters(
#     host=<class 'pika.connection.ConnectionParameters._DEFAULT'>,
#     port=<class 'pika.connection.ConnectionParameters._DEFAULT'>,
#     virtual_host=<class 'pika.connection.ConnectionParameters._DEFAULT'>,
#     credentials=<class 'pika.connection.ConnectionParameters._DEFAULT'>,
#     channel_max=<class 'pika.connection.ConnectionParameters._DEFAULT'>,
#     frame_max=<class 'pika.connection.ConnectionParameters._DEFAULT'>,
#     heartbeat=<class 'pika.connection.ConnectionParameters._DEFAULT'>,
#     ssl_options=<class 'pika.connection.ConnectionParameters._DEFAULT'>,
#     connection_attempts=<class 'pika.connection.ConnectionParameters._DEFAULT'>,
#     retry_delay=<class 'pika.connection.ConnectionParameters._DEFAULT'>,
#     socket_timeout=<class 'pika.connection.ConnectionParameters._DEFAULT'>,
#     stack_timeout=<class 'pika.connection.ConnectionParameters._DEFAULT'>,
#     locale=<class 'pika.connection.ConnectionParameters._DEFAULT'>,
#     blocked_connection_timeout=<class 'pika.connection.ConnectionParameters._DEFAULT'>,
#     client_properties=<class 'pika.connection.ConnectionParameters._DEFAULT'>,
#     tcp_options=<class 'pika.connection.ConnectionParameters._DEFAULT'>,
#     **kwargs)
parameters = pika.ConnectionParameters('localhost', credentials=credentials)

# class pika.adapters.blocking_connection.BlockingConnection(parameters=None, _impl_class=None)
connection = pika.BlockingConnection(parameters)

# channel(channel_number=None)
channel = connection.channel()

# exchange_declare(
#     exchange,
#     exchange_type=<ExchangeType.direct: 'direct'>,
#     passive=False,
#     durable=False,
#     auto_delete=False,
#     internal=False,
#     arguments=None)
channel.exchange_declare(exchange="test_exchange",
                         exchange_type=ExchangeType.direct,
                         passive=False,
                         durable=True,
                         auto_delete=False)

print("Sending message to create a queue")

# basic_publish(exchange, routing_key, body, properties=None, mandatory=False)
# class pika.spec.BasicProperties(
#     content_type=None,
#     content_encoding=None,
#     headers=None,
#     delivery_mode=None,
#     priority=None,
#     correlation_id=None,
#     reply_to=None,
#     expiration=None,
#     message_id=None,
#     timestamp=None,
#     type=None,
#     user_id=None,
#     app_id=None,
#     cluster_id=None)
channel.basic_publish(
    'test_exchange', 'standard_key', 'queue:group',
    pika.BasicProperties(content_type='text/plain',
                         delivery_mode=DeliveryMode.Transient))

connection.sleep(5)

print("Sending text message to group")

channel.basic_publish(
    'test_exchange', 'group_key', 'Message to group_key',
    pika.BasicProperties(content_type='text/plain',
                         delivery_mode=DeliveryMode.Transient))

connection.sleep(5)

print("Sending text message")

channel.basic_publish(
    'test_exchange', 'standard_key', 'Message to standard_key',
    pika.BasicProperties(content_type='text/plain',
                         delivery_mode=DeliveryMode.Transient))

connection.close()
