from database import Base
from sqlalchemy import Column, Integer, Boolean, Text, String, ForeignKey
from sqlalchemy_utils.types import ChoiceType
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(25), unique=True)
    email = Column(String(80), unique=True)
    password = Column(Text, nullable=True)
    is_staff = Column(Boolean, default=False)
    is_active = Column(Boolean, default=False)
    orders = relationship('Order', back_populates='user')

    def __repr__(self):
        return f"<User {self.username}>"


class Order(Base):

    ORDER_STATUS = (
        ('pending', 'pending'),
        ('in-transit', 'in-transit'),
        ('delivered', 'delivered')
    )

    PIZZA_SIZE = (
        ('small', 'small'),
        ('medium', 'medium'),
        ('large', 'large')
    )

    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    quantity = Column(Integer, nullable=False)
    status = Column(ChoiceType(choices=ORDER_STATUS, impl=String()), default='pending')
    pizza_size = Column(ChoiceType(choices=PIZZA_SIZE, impl=String()), default='medium')
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='orders')

    def __repr__(self):
        return f"<Order: {self.id}>"