# -*- coding: utf-8 -*-
# pylint: disable=C0111,C0103,R0205

import json
import logging
import pika
from pika.exchange_type import ExchangeType

print('pika version: %s' % pika.__version__)

# class pika.adapters.blocking_connection.BlockingConnection(parameters=None, _impl_class=None)
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
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))

# channel(channel_number=None)
main_channel = connection.channel()
consumer_channel = connection.channel()
bind_channel = connection.channel()

main_channel.exchange_declare(exchange='com.micex.sten', exchange_type=ExchangeType.direct)
main_channel.exchange_declare(
    exchange='com.micex.lasttrades', exchange_type=ExchangeType.direct)

# queue_declare(queue, passive=False, durable=False, exclusive=False, auto_delete=False, arguments=None)
queue = main_channel.queue_declare('', exclusive=True).method.queue
queue_tickers = main_channel.queue_declare('', exclusive=True).method.queue

main_channel.queue_bind(
    exchange='com.micex.sten', queue=queue, routing_key='order.stop.create')


def hello():
    print('Hello world')

# call_later(delay, callback)
connection.call_later(5, hello)


def callback(_ch, _method, _properties, body):
    body = json.loads(body)['order.stop.create']

    ticker = None
    if 'ticker' in body['data']['params']['condition']:
        ticker = body['data']['params']['condition']['ticker']
    if not ticker:
        return

    print('got ticker %s, gonna bind it...' % ticker)
    bind_channel.queue_bind(
        exchange='com.micex.lasttrades',
        queue=queue_tickers,
        routing_key=str(ticker))
    print('ticker %s binded ok' % ticker)


logging.basicConfig(level=logging.INFO)

# Note: consuming with automatic acknowledgements has its risks
#       and used here for simplicity.
#       See https://www.rabbitmq.com/confirms.html.
# basic_consume(queue, on_message_callback, auto_ack=False, exclusive=False, consumer_tag=None, arguments=None)
consumer_channel.basic_consume(queue, callback, auto_ack=True)

try:
    consumer_channel.start_consuming()
finally:
    connection.close()
