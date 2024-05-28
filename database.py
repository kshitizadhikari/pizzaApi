import pymongo
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# client = pymongo.MongoClient("mongodb://localhost:27017/")
#
# db = client['pizza_db']
#
# pizzaCol = db['pizza']
# users = db['user']


engine = create_engine("postgresql://postgres:admin@localhost/pizza_db",
                       echo=True
                       )

Base = declarative_base()
Session = sessionmaker()

