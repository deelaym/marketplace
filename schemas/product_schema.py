from pydantic import BaseModel


class ProductSchema(BaseModel):
    category_id: int | None = None
    name: str | None = None
    photo_url: str | None = None
    description: str | None = None
    amount: int | None = None
    price: float | None = None
    discount: int | None = None