from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from .database import Base


class ProductsInOrder(Base):
    __tablename__ = 'products_in_orders'
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.product_id'))
    amount = Column(Integer)
    products = relationship('Product', backref='products')
