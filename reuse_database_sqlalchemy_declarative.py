# https://techarena51.com/index.php/flask-sqlalchemy-postgresql-tutorial/
# http://pythoncentral.io/introductory-tutorial-python-sqlalchemy/

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
    title = Column(String(50000))
    author = Column(String(500))
    author_birth = Column(Integer)
    author_death = Column(Integer)
    language = Column(String(500))
    publication_year = Column(Integer)
    publication_place = Column(String(500))
    country = Column(String(500))
    publisher = Column(String(5000))


class Extract(Base):
    __tablename__ = 'extract'

    id = Column(Integer, primary_key=True)
    text = Column(String(500000))
    cluster_id = Column(Integer, ForeignKey('cluster.id'))
    cluster = relationship(Cluster)
    book_id = Column(String(250), ForeignKey('book.id'))
    book = relationship(Book)
    ecco_id = Column(String(250))


# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
# dbstring_sqlite = 'sqlite:///sqlalchemy_text_reuse.db'
dbstring_postgresql = (
    'postgresql://text_reuse_user:randompass@localhost:5432/text_reuse')
engine = create_engine(dbstring_postgresql)

# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)
