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
    avglength = Column(Integer, index=True)
    count = Column(Integer, index=True)
    text = Column(String(500000))
    # name = Column(String(250), nullable=False)


class Book(Base):
    __tablename__ = 'book'

    id = Column(String(250), primary_key=True)  # estc id
    title = Column(String(50000), index=True)
    author = Column(String(500), index=True)
    author_birth = Column(Integer)
    author_death = Column(Integer)
    language = Column(String(500))
    publication_year = Column(Integer, index=True)
    publication_place = Column(String(500))
    country = Column(String(500))
    publisher = Column(String(5000))


class Extract(Base):
    __tablename__ = 'extract'

    id = Column(Integer, primary_key=True)
    cluster_id = Column(Integer, ForeignKey('cluster.id'), index=True)
    cluster = relationship(Cluster)
    book_id = Column(String(250), ForeignKey('book.id'), index=True)
    book = relationship(Book)
    ecco_id = Column(String(250), index=True)


# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
dbstring_sqlite = 'sqlite:///sqlalchemy_text_reuse.db'
dbstring_postgresql = (
    'postgresql://text_reuse_user:randompass@localhost:5432/text_reuse')
engine = create_engine(dbstring_sqlite)

# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)
