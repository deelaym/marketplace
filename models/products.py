from sqlalchemy import Column, Integer, String, Text, ForeignKey, Numeric, CheckConstraint
from sqlalchemy.orm import relationship

from .database import Base


class Product(Base):
    __tablename__ = 'products'
    product_id = Column(Integer, primary_key=True)
    shop_id = Column(Integer, ForeignKey('shops.shop_id'))
    category_id = Column(Integer, ForeignKey('categories.category_id'))
    name = Column(String)
    photo_url = Column(String)
    description = Column(Text)
    amount = Column(Integer)
    price = Column(Numeric(10, 2))
    discount = Column(Integer)
    shop = relationship('Shop', backref='shop')
    category = relationship('Category', backref='category')


    __table_args__ = (
        CheckConstraint('discount >= 0 And discount < 100', name='check_discount_range'),
    )

