import asyncio
import json

from aio_pika import IncomingMessage

from logger import log
from rabbitmq.config import get_connection, NEW_ORDERS_QUEUE
from routers.orders_router import change_order_status


async def process_order(message: IncomingMessage):
    async with message.process():
        order = json.loads(message.body)
        await change_order_status(order, order['status_id'] + 1)
        log.info(f'Order {order['order_id']} changed status to {order['status_id'] + 1}')


async def start_consuming():
    connection = await get_connection()
    async with connection:
        async with connection.channel() as channel:
            queue = await channel.declare_queue(name=NEW_ORDERS_QUEUE, durable=True)

            await queue.consume(process_order)
            await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(start_consuming())