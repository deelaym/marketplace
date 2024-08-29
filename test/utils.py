

def shop_to_dict(shop):
    return {
        'shop_id': shop.shop_id,
        'name': shop.name,
        'description': shop.description,
        'photo_url': shop.photo_url,
        'created_at': shop.created_at,
        'updated_at': shop.updated_at
    }


def product_to_dict(product):
    return {
        'product_id': product.product_id,
        'shop_id': product.shop_id,
        'category_id': product.category_id,
        'name': product.name,
        'photo_url': product.photo_url,
        'description': product.description,
        'amount': product.amount,
        'price': product.price,
        'discount': product.discount,
        'created_at': product.created_at,
        'updated_at': product.updated_at
    }