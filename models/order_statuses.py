from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

from .database import Base


class OrderStatus(Base):
    __tablename__ = 'order_statuses'
    status_id = Column(Integer, primary_key=True)
    status_name = Column(String)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)
    orders = relationship("Order", backref='orders_by_status')
