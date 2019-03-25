from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import create_engine

Base = declarative_base()

class Restaurant(Base):
    __tablename__='restaurant'
    id = Column(Integer, primary_key=True)
    name=Column(String(50),nullable=False)



class MenuItem(Base):
    __tablename__ = 'menuitem'
    id = Column(Integer,primary_key=True)
    name = Column(String(50))
    description=Column(String(80))
    price = Column(String(10))
    course = Column(String(250))

    
    restaurant_id = Column(Integer,ForeignKey('restaurant.id'))
    restaurant = relationship(Restaurant)




engine = create_engine('sqlite:///restaurantmenu.db')

Base.metadata.create_all(engine)