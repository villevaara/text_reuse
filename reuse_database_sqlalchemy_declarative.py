# https://techarena51.com/index.php/flask-sqlalchemy-postgresql-tutorial/
# http://pythoncentral.io/introductory-tutorial-python-sqlalchemy/

# import os
# import sys

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Cluster(Base):
    __tablename__ = 'cluster'
    id = Column(Integer, primary_key=True)
    avglength = Column(Integer)
    count = Column(Integer)
    # name = Column(String(250), nullable=False)


class Book(Base):
    __tablename__ = 'book'
    id = Column(String(250), primary_key=True)  # estc id
    title = Column(String(250))
    author = Column(String(250))
    author_birth = Column(Integer)
    author_death = Column(Integer)
    language = Column(String(250))
    publication_year = Column(Integer)
    publication_place = Column(String(250))
    country = Column(String(250))
    publisher = Column(String(250))


class Extract(Base):
    __tablename__ = 'extract'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    # id = Column(String(250), primary_key=True)
    id = Column(Integer, primary_key=True)
    text = Column(String(5000))
    cluster_id = Column(Integer, ForeignKey('cluster.id'))
    cluster = relationship(Cluster)
    book_id = Column(Integer, ForeignKey('book.id'))
    book = relationship(Book)
    ecco_id = Column(String(250))


# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
engine = create_engine('sqlite:///sqlalchemy_text_reuse.db')

# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)
