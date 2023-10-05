#!/usr/bin/python3
"""Database Storage module for HBNB project"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from os import getenv
from sqlalchemy.ext.declarative import declarative_base
#Base = declarative_base()
from models import base_model
from models.city import City
from models.state import State
from models.base_model import BaseModel
from models.base_model import Base
from models.place import Place
from models.review import Review
from models.user import User
from models.amenity import Amenity

class DBStorage:
    """Database Storage class"""
    __engine = None
    __session = None

    def __init__(self):
        """Initialize a new DBStorage instance."""
        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}/{}".format(
            getenv("HBNB_MYSQL_USER"),
            getenv("HBNB_MYSQL_PWD"),
            getenv("HBNB_MYSQL_HOST"),
            getenv("HBNB_MYSQL_DB")),
            pool_pre_ping=True)
        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query all objects in the database"""
        session = self.__session
        objects = {}

        if cls is None:
            classes = [City, State]

            for model_class in classes:
                results = session.query(model_class).all()
                for obj in results:
                    key = "{}.{}".format(obj.__class__.__name__, obj.id)
                    objects[key] = obj
        else:
            results = session.query(cls).all()
            for obj in results:
                key = "{}.{}".format(obj.__class__.__name__, obj.id)
                objects[key] = obj
        return objects

    def new(self, obj):
        """Add the object to the current database session"""
        session = self.__session
        session.add(obj)

    def save(self):
        """Commit all changes of the current database session"""
        session = self.__session
        session.commit()

    def delete(self, obj=None):
        """Delete obj from the current database session"""
        if obj is not None:
            session = self.__session
            session.delete(obj)

    def reload(self):
        """Create all tables in the database and create the current database session"""
        engine = self.__engine
        Session = scoped_session(sessionmaker(bind=engine, expire_on_commit=False))
        self.__session = Session()

        base_model.Base.metadata.create_all(engine)

    def close(self):
        """Close the current database session"""
        if self.__session:
            self.__session.close()
