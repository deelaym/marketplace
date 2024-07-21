from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class Category(Base):
    __tablename__ = 'categories'
    category_id = Column(Integer, primary_key=True)
    name = Column(String)
    products = relationship('Product', backref='products')

