from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship

from .database import Base


class Shop(Base):
    __tablename__ = 'shops'
    shop_id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(Text)
    photo_url = Column(String)
    products = relationship('Product', backref='products')
