import os

import aio_pika
from aio_pika.abc import AbstractRobustConnection, AbstractRobustChannel
from dotenv import load_dotenv

load_dotenv()

NEW_ORDERS_QUEUE = 'new_orders_queue'
PROCESSING_ORDERS_QUEUE = 'processing_orders_queue'
SENDING_NOTIFICATIONS_QUEUE = 'sending_notifications_queue'

RMQ_HOST = os.getenv('RMQ_HOST')
RMQ_USER = os.getenv('RMQ_USER')
RMQ_PASS = os.getenv('RMQ_PASS')


async def get_connection() -> AbstractRobustConnection:
    connection = await aio_pika.connect_robust(f"amqp://{RMQ_USER}:{RMQ_PASS}@{RMQ_HOST}/")
    return connection


async def declare_queues(channel: AbstractRobustChannel):
    queues = [NEW_ORDERS_QUEUE, PROCESSING_ORDERS_QUEUE, SENDING_NOTIFICATIONS_QUEUE]
    for queue in queues:
        await channel.declare_queue(name=queue, durable=True)
