from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship

from .database import Base


class Shop(Base):
    __tablename__ = 'shops'
    shop_id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(Text)
    photo_url = Column(String)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)
    products = relationship('Product', backref='shop_products')
