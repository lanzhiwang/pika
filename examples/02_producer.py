# -*- coding: utf-8 -*-
# pylint: disable=C0111,C0103,R0205

import json
import random
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

main_channel = connection.channel()

# exchange_declare(
#     exchange,
#     exchange_type=<ExchangeType.direct: 'direct'>,
#     passive=False,
#     durable=False,
#     auto_delete=False,
#     internal=False,
#     arguments=None)
main_channel.exchange_declare(exchange='com.micex.sten', exchange_type=ExchangeType.direct)
main_channel.exchange_declare(
    exchange='com.micex.lasttrades', exchange_type=ExchangeType.direct)

tickers = {
    'MXSE.EQBR.LKOH': (1933, 1940),
    'MXSE.EQBR.MSNG': (1.35, 1.45),
    'MXSE.EQBR.SBER': (90, 92),
    'MXSE.EQNE.GAZP': (156, 162),
    'MXSE.EQNE.PLZL': (1025, 1040),
    'MXSE.EQNL.VTBR': (0.05, 0.06)
}


def getticker():
    return list(tickers.keys())[random.randrange(0, len(tickers) - 1)]


_COUNT_ = 10

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
for i in range(0, _COUNT_):
    ticker = getticker()
    msg = {
        'order.stop.create': {
            'data': {
                'params': {
                    'condition': {
                        'ticker': ticker
                    }
                }
            }
        }
    }
    main_channel.basic_publish(
        exchange='com.micex.sten',
        routing_key='order.stop.create',
        body=json.dumps(msg),
        properties=pika.BasicProperties(content_type='application/json'))
    print('send ticker %s' % ticker)

connection.close()
