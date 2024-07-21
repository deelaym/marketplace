from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class OrderStatus(Base):
    __tablename__ = 'order_statuses'
    status_id = Column(Integer, primary_key=True)
    status_name = Column(String)
    orders = relationship("Order", backref='orders')
