from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.categories import Category
from models.database import get_async_session
from models.products import Product
from schemas.category_schema import CategorySchema

category_router = APIRouter(
    tags=['Categories']
)


@category_router.post('/create')
async def create_category(category: CategorySchema,
                          session: AsyncSession = Depends(get_async_session)):
    category = Category(**category.dict())
    session.add(category)
    await session.commit()
    return {'status': 200, 'category': category}


@category_router.get('/{category_name}')
async def get_product_list_by_category(category_name: str,
                                       limit: int = 10,
                                       offset: int = 0,
                                       session: AsyncSession = Depends(get_async_session)):
    query = select(Product).join(Category).where(Category.name == category_name)
    products = (await session.scalars(query)).all()[offset:offset+limit]
    return {'status': 200, 'product_list': products}
