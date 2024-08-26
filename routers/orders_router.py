from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.database import get_async_session
from models.orders import Order
from models.products_in_order import ProductsInOrder
from rabbitmq.publisher import send_order, send_notification, processing_order
from schemas.MessageSchema import StatusMessageSchema
from schemas.order_schema import OrderFullSchema

orders_router = APIRouter(
    tags=['Orders']
)


@orders_router.post('/create')
async def create_new_order(order_data: OrderFullSchema,
                           session: AsyncSession = Depends(get_async_session)
                           ):
    try:
        new_order = Order(**order_data.dict(exclude={'products_in_order', 'order_id'}))
        session.add(new_order)
        await session.commit()

        products = [ProductsInOrder(order_id=new_order.order_id, **product.dict()) for product in order_data.products_in_order]
        for product in products:
            session.add(product)
        await session.commit()

        order_data.order_id = new_order.order_id
        await send_order(order_data)
        return {'status': 200, 'new_order': new_order, 'products': products}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}


@orders_router.post('/change_status')
async def change_order_status(order_data: OrderFullSchema,
                              status_id: int,
                              session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(Order).where(Order.order_id == order_data.order_id)
        order = await session.scalar(query)

        order.status_id = status_id
        session.add(order)
        await session.commit()
        order_data.status_id = status_id

        message = StatusMessageSchema(
            text=f'Order {order.order_id} changed status to {status_id}',
            status_id=status_id,
            order_id=order.order_id
        )

        await send_notification(message)
        await processing_order(order_data)

        return {'status': 200, 'order': order_data}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}
