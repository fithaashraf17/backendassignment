

# imports
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()
path = os.path.dirname(os.path.dirname(__file__)) + '/my_cart.db'
engine = create_engine('sqlite:///' + path)
DBSession = sessionmaker(bind=engine)
session = DBSession()


class User(Base):
    """
    A database model for client_details table
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String)
    name = Column(String)
    email = Column(String, nullable=True)
    password = Column(String)
    created_on = Column('created_on', DateTime, server_default=func.now())
    updated_on = Column('updated_on', DateTime, onupdate=func.now())

    cart = relationship("Cart", back_populates='user', cascade="all, delete, delete-orphan")
    order = relationship("Order", back_populates='user', cascade="all, delete, delete-orphan")

    def __repr__(self):
        return str(self.id)


class Category(Base):
    """
    A database model for client_details table
    """

    __tablename__ = "categories"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True)
    created_on = Column('created_on', DateTime, server_default=func.now())
    updated_on = Column('updated_on', DateTime, onupdate=func.now())

    products = relationship("Product", back_populates='category', cascade="all, delete, delete-orphan")

    def __repr__(self):
        """
        Object String representation
    
        """
        return str(self.name)


class Cart(Base):
    """
    A database model for client_details table
    """

    __tablename__ = "cart"
    id = Column(Integer, primary_key=True)
    created_on = Column('created_on', DateTime, server_default=func.now())
    updated_on = Column('updated_on', DateTime, onupdate=func.now())
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates='cart')
    product_id = Column(Integer, ForeignKey('products.id'), nullable=True)
    products = relationship("Product", back_populates="cart")

    def __repr__(self):
        """
        Object String representation
        :return:
        """
        return str(self.id)


class Product(Base):
    """
    A database model for client_details table
    """

    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=True)
    created_on = Column('created_on', DateTime, server_default=func.now())
    updated_on = Column('updated_on', DateTime, onupdate=func.now())
    category_id = Column(Integer, ForeignKey('categories.id'))

    category = relationship("Category", back_populates="products")
    cart = relationship("Cart", back_populates='products')

    def __repr__(self):
        """
        Object String representation
 
        """
        return str(self.name)


class Order(Base):
    """
    A database model for client_details table
    """

    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    order_date = Column('order_date', DateTime, nullable=True)
    status = Column('status', String)
    user_id = Column(Integer, ForeignKey('users.id'))

    created_on = Column('created_on', DateTime, server_default=func.now())
    updated_on = Column('updated_on', DateTime, onupdate=func.now())
    bill = relationship("Bill", back_populates="order", cascade="all, delete, delete-orphan")
    user = relationship("User", back_populates="order")

    def __repr__(self):
        """
        Object String representation
  
        """
        return str(self.id)


class Bill(Base):
    """
    A database model for client_details table
    """

    __tablename__ = "bill"
    id = Column(Integer, primary_key=True)
    cart_value = Column(Float)
    discount = Column(Float)
    sub_total = Column(Float)
    created_on = Column('created_on', DateTime, server_default=func.now())
    updated_on = Column('updated_on', DateTime, onupdate=func.now())

    order_id = Column(Integer, ForeignKey('orders.id'))
    order = relationship("Order", back_populates="bill")

    def __repr__(self):
        """
        Object String representation
   
        """
        return str(self.id)
