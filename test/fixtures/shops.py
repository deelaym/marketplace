from datetime import datetime

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.categories import Category
from models.products import Product
from models.shops import Shop
from schemas.product_schema import ProductSchema
from schemas.shop_schema import ShopSchema


@pytest.fixture
async def shop_info_1() -> ShopSchema:
    shop = ShopSchema(
        name='Shop_1',
        description='description_1',
        photo_url='photo_url_1'
    )
    return shop


@pytest.fixture
async def shop_1(shop_info_1: ShopSchema, session: AsyncSession) -> Shop:
    shop = Shop(
        **shop_info_1.dict(),
        created_at=datetime(2024, 8, 1, 0, 42, 42),
        updated_at=datetime(2024, 8, 1, 0, 42, 42),
    )

    session.add(shop)
    await session.commit()
    await session.close()
    return shop


@pytest.fixture
async def shop_2(session: AsyncSession) -> Shop:
    shop = Shop(
        name='Shop_2',
        description='description_2',
        photo_url='photo_url_2',
        created_at=datetime(2024, 8, 1, 0, 42, 42),
        updated_at=datetime(2024, 8, 1, 0, 42, 42),
    )

    session.add(shop)
    await session.commit()
    await session.close()
    return shop


@pytest.fixture
async def product_info_1(category_1: Category) -> ProductSchema:
    product = ProductSchema(
        category_id=category_1.category_id,
        name='Product_1',
        photo_url='url',
        description='description_1',
        amount=42,
        price=666,
        discount=0
    )
    return product


@pytest.fixture
async def product_1(shop_1: Shop,
                    product_info_1: ProductSchema,
                    session: AsyncSession):
    product = Product(**product_info_1.dict(), shop_id=shop_1.shop_id)
    session.add(product)
    await session.commit()
    await session.close()
    return product


@pytest.fixture
async def product_2(shop_1: Shop,
                    category_1: Category,
                    session: AsyncSession):
    product = Product(shop_id=shop_1.shop_id,
                      category_id=category_1.category_id,
                      name='Product_2',
                      photo_url='url2',
                      description='description_2',
                      amount=42,
                      price=666,
                      discount=0
                      )
    session.add(product)
    await session.commit()
    await session.close()
    return product
