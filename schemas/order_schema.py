from typing import List

from pydantic import BaseModel


class ProductInOrderSchema(BaseModel):
    product_id: int
    amount: int


class OrderFullSchema(BaseModel):
    order_id: int | None = None
    user_id: int
    products_in_order: List[ProductInOrderSchema]
    status_id: int = 1

    class Config:
        from_attributes = True


