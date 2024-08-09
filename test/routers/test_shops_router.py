from unittest.mock import patch, AsyncMock

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from models.products import Product
from models.shops import Shop
from routers.shops_router import get_shop_list, create_new_shop, add_product_to_shop, delete_product, update_product, \
    get_product, get_product_list_by_shop, get_shop
from schemas.product_schema import ProductSchema
from schemas.shop_schema import ShopSchema
from test.utils import shop_to_dict, product_to_dict


async def test_get_shop_list(shop_1: Shop, shop_2: Shop, session: AsyncSession):
    result = await get_shop_list(session=session)
    await session.close()
    assert result['status'] == 200
    assert 'shop_list' in result

    result_list = [shop_to_dict(shop) for shop in result['shop_list']]

    assert result_list == [shop_to_dict(shop) for shop in [shop_1, shop_2]]


async def test_create_new_shop(shop_info_1: ShopSchema, session: AsyncSession):
    result = await create_new_shop(shop_info_1, session)
    await session.close()
    assert result['status'] == 200
    assert 'new_shop' in result

    assert result['new_shop'].shop_id == 1
    assert result['new_shop'].name == shop_info_1.name
    assert result['new_shop'].description == shop_info_1.description
    assert result['new_shop'].photo_url == shop_info_1.photo_url


@pytest.mark.parametrize('shop_id', [1, pytest.param(42, marks=pytest.mark.xfail)])
async def test_get_shop(shop_1: Shop, shop_id: int, session: AsyncSession):
    result = await get_shop(shop_id, session)
    await session.close()
    assert result['status'] == 200
    assert result['shop'].shop_id == shop_id


async def test_add_product_to_shop_success(shop_1: Shop,
                                           product_info_1: ProductSchema,
                                           session: AsyncSession):
    result = await add_product_to_shop(shop_1.shop_id, product_info_1, session)
    await session.close()

    assert result['status'] == 200
    product = result['new_product']
    expected_data = {'shop_id': shop_1.shop_id,
                     'product_id': 1}
    expected_data.update(product_info_1.dict())
    product_data = product_to_dict(product)
    product_data.pop('created_at')
    product_data.pop('updated_at')
    assert product_data == expected_data


async def test_add_product_to_shop_fail(product_info_1: ProductSchema,
                                        session: AsyncSession):
    result = await add_product_to_shop(42, product_info_1, session)
    await session.close()

    assert result['status'] == 'error'


async def test_delete_product_product_exists(shop_1: Shop,
                                             product_1: Product):
    mock_session = AsyncMock(spec=AsyncSession)
    mock_session.get.return_value = product_1

    result = await delete_product(shop_1.shop_id, product_1.product_id, mock_session)
    mock_session.delete.assert_called_once_with(product_1)

    assert result['status'] == 200


async def test_delete_product_product_does_not_exist(shop_1: Shop,
                                                     session: AsyncSession):
    result = await delete_product(shop_1.shop_id, 42, session)
    await session.close()
    assert result['status'] == 404
    assert result['message'] == 'Product not found'


async def test_update_product_product_exists(shop_1: Shop,
                                             product_1: Product,
                                             session: AsyncSession):
    product_update = ProductSchema(
        name='424242',
        amount=10000,
        photo_url='photo'
    )
    result = await update_product(shop_1.shop_id, product_1.product_id, product_update, session)
    await session.close()
    assert result['status'] == 200

    product = result['product']
    assert product.name == product_update.name
    assert product.amount == product_update.amount
    assert product.photo_url == product_update.photo_url
    assert product.category_id is not None


async def test_update_product_product_does_not_exist(shop_1: Shop,
                                                     session: AsyncSession):
    product_update = ProductSchema(
        name='424242'
    )
    result = await update_product(shop_1.shop_id, 42, product_update, session)
    await session.close()
    assert result['status'] == 404
    assert result['message'] == 'Product not found'


@pytest.mark.parametrize('product_id', [1, 2, pytest.param(42, marks=pytest.mark.xfail)])
async def test_get_product_product_exists(product_1: Product,
                                          product_2: Product,
                                          product_id: int,
                                          session: AsyncSession):
    result = await get_product(product_1.shop_id, product_id, session)
    await session.close()
    assert result['status'] == 200
    assert result['product'].product_id == product_id


async def test_get_product_product_does_not_exist(session: AsyncSession):
    result = await get_product(1, 42, session)
    await session.close()
    assert result['status'] == 404
    assert result['message'] == 'Product not found'


async def test_get_product_list_by_shop_success(shop_1: Shop,
                                                product_1: Product,
                                                session: AsyncSession):

    mock_response = {'status': 200}
    with patch('routers.shops_router.get_shop', return_value=mock_response):
        result = await get_product_list_by_shop(shop_1.shop_id, session=session)
        await session.close()
        assert result['status'] == 200
        products = result['product_list']
        assert products[0].product_id == product_1.product_id


async def test_get_product_list_by_shop_wrong_shop_id(session: AsyncSession):
    result = await get_product_list_by_shop(42, session=session)
    await session.close()
    assert result['status'] == 'error'
    assert result['message'] == 'Shop not found'

