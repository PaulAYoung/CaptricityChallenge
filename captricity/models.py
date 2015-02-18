from flask.ext.login import UserMixin
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from captricity.config import db_uri

engine = create_engine(db_uri, echo=False, convert_unicode=False)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))


class DBBase(object):
    """
    Default attributes for all tables
    """
    #All tables should have an id column
    id = Column(Integer, primary_key=True)


Base = declarative_base(cls=DBBase)
Base.query = db_session.query_property()


#UserMixin class makes this work with flask-login
class User(Base, UserMixin):
    __tablename__ = 'users'
    username = Column(String(50), index=True, unique=True)
    password = Column(String(256))


class Batch(Base):
    __tablename__ = 'batches'
    batch_id = Column(Integer)
    status = Column(String(50))
    extract = Column(Text)


class Image(Base):
    __tablename__ = 'images'
    title = Column(String(100))
    path = Column(String(1024))
    user = Column(Integer, ForeignKey(User.id))
    batch = Column(Integer, ForeignKey(Batch.id))
