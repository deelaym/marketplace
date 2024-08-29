from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from models.database import get_async_session
from models.products import Product
from models.shops import Shop
from schemas.product_schema import ProductSchema
from schemas.shop_schema import ShopSchema

shops_router = APIRouter(
    tags=['Shops']
)


@shops_router.get('/')
async def get_shop_list(limit: int = 10,
                        offset: int = 0,
                        session: AsyncSession = Depends(get_async_session)):
    query = select(Shop).order_by(Shop.shop_id)
    result = (await session.scalars(query)).all()[offset:offset+limit]
    return {'status': 200, 'shop_list': result}


@shops_router.post('/create')
async def create_new_shop(shop_info: ShopSchema, session: AsyncSession = Depends(get_async_session)):
    try:
        new_shop = Shop(**shop_info.dict())
        session.add(new_shop)
        await session.commit()
        return {'status': 200, 'new_shop': new_shop}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}


@shops_router.get('/{shop_id}')
async def get_shop(shop_id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(Shop).where(Shop.shop_id == shop_id)
    shop = await session.scalar(query)
    if shop:
        return {'status': 200, 'shop': shop}
    return {'status': 'error', 'message': 'Shop not found'}


@shops_router.post('/{shop_id}/add_product')
async def add_product_to_shop(shop_id: int,
                              product: ProductSchema,
                              session: AsyncSession = Depends(get_async_session)):
    new_product = Product(shop_id=shop_id, **product.dict())
    try:
        session.add(new_product)
        await session.commit()
        return {'status': 200, 'new_product': new_product}
    except IntegrityError as e:
        return {'status': 'error', 'message': str(e.orig)}


@shops_router.delete('/{shop_id}/product/{product_id}/delete')
async def delete_product(shop_id: int,
                         product_id: int,
                         session: AsyncSession = Depends(get_async_session)):
    product = await session.get(Product, product_id)
    if product:
        await session.delete(product)
        await session.commit()
        return {'status': 200}
    return {'status': 404, 'message': 'Product not found'}


@shops_router.patch('/{shop_id}/product/{product_id}/update')
async def update_product(shop_id: int,
                         product_id: int,
                         product_update: ProductSchema,
                         session: AsyncSession = Depends(get_async_session)):
    query = select(Product).where(Product.product_id == product_id)
    product = await session.scalar(query)
    if product:
        for key, val in product_update.dict().items():
            if hasattr(product, key) and val is not None:
                setattr(product, key, val)
        product.updated_at = datetime.now()
        await session.commit()
        return {'status': 200, 'product': product}
    return {'status': 404, 'message': 'Product not found'}


@shops_router.get('/{shop_id}/product/{product_id}')
async def get_product(shop_id: int,
                      product_id: int,
                      session: AsyncSession = Depends(get_async_session)):
    product = await session.get(Product, product_id)
    if product:
        return {'status': 200, 'product': product}
    return {'status': 404, 'message': 'Product not found'}


@shops_router.get('/{shop_id}/products')
async def get_product_list_by_shop(shop_id: int,
                                   limit: int = 10,
                                   offset: int = 0,
                                   session: AsyncSession = Depends(get_async_session)):
    try:
        shop_response = await get_shop(shop_id, session)
        if shop_response['status'] == 200:
            query = select(Product).where(Product.shop_id == shop_id)
            products = (await session.scalars(query)).all()[offset:offset+limit]
            return {'status': 200, 'product_list': products}
        return shop_response
    except Exception as e:
        return {'status': 'error', 'message': str(e)}









