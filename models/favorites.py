from sqlalchemy import Column, Integer, ForeignKey

from .database import Base


class Favorites(Base):
    __tablename__ = 'favorites'
    user_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)
    product_id = Column(Integer, ForeignKey('products.product_id'))
