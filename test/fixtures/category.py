import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from models.categories import Category
from schemas.category_schema import CategorySchema


@pytest.fixture
async def category_info_1() -> CategorySchema:
    category = CategorySchema(
        name='Category_1'
    )
    return category


@pytest.fixture
async def category_1(category_info_1, session: AsyncSession) -> Category:
    category = Category(**category_info_1.dict())
    session.add(category)
    await session.commit()
    await session.close()
    return category

