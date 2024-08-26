from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from .database import Base


class Order(Base):
    __tablename__ = 'orders'
    order_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now)
    status_id = Column(Integer, ForeignKey('order_statuses.status_id'))
    user = relationship('User', backref='user')
    status = relationship('OrderStatus', backref='status')


