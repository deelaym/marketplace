from typing import TYPE_CHECKING

import aio_pika

from logger import log
from rabbitmq.config import get_connection, declare_queues, NEW_ORDERS_QUEUE, SENDING_NOTIFICATIONS_QUEUE, \
    PROCESSING_ORDERS_QUEUE
from schemas.order_schema import OrderFullSchema

if TYPE_CHECKING:
    from aio_pika.abc import AbstractRobustChannel


async def publish_message(channel: 'AbstractRobustChannel', queue_name: str, message: OrderFullSchema):
    await channel.default_exchange.publish(
        message=aio_pika.Message(message.json().encode()),
        routing_key=queue_name,
    )
    log.info('%s published', message)


async def send_order(order, ):
    connection = await get_connection()
    async with connection:
        async with connection.channel() as channel:
            await declare_queues(channel)
            await publish_message(channel, NEW_ORDERS_QUEUE, order)


async def send_notification(message):
    connection = await get_connection()
    async with connection:
        async with connection.channel() as channel:
            await declare_queues(channel)
            await publish_message(channel, SENDING_NOTIFICATIONS_QUEUE, message)


async def processing_order(order, ):
    connection = await get_connection()
    async with connection:
        async with connection.channel() as channel:
            await declare_queues(channel)
            await publish_message(channel, PROCESSING_ORDERS_QUEUE, order)

