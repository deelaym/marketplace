import asyncio
import json
import os

import aiohttp
from aio_pika import IncomingMessage

from logger import log
from config import get_connection, NEW_ORDERS_QUEUE
from dotenv import load_dotenv

load_dotenv()

APP_HOST = os.getenv('APP_HOST')
APP_PORT = os.getenv('APP_PORT')


async def process_order(message: IncomingMessage):
    async with message.process():
        order = json.loads(message.body)
        async with aiohttp.ClientSession() as session:
            async with session.post(f'http://{APP_HOST}:{APP_PORT}/orders/change_status?status_id={order["status_id"] + 1}',
                                    json=order) as response:
                if response.status == 200:
                    log.info(f'Order {order['order_id']} changed status to {order['status_id'] + 1}')
                    log.info(await response.json())
                else:
                    log.error(await response.json())


async def start_consuming():
    connection = await get_connection()
    async with connection:
        async with connection.channel() as channel:
            queue = await channel.declare_queue(name=NEW_ORDERS_QUEUE, durable=True)

            await queue.consume(process_order)
            await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(start_consuming())