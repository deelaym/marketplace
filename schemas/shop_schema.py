from pydantic import BaseModel


class ShopSchema(BaseModel):
    name: str
    description: str
    photo_url: str

    class Config:
        from_attributes = True
