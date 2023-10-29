from sqlalchemy import Column, Integer, String

from database import Base


class Dog(Base):
    __tablename__ = "dogs"

    name = Column(String)
    pk = Column(Integer, primary_key=True, unique=True)
    kind = Column(String)


class Timestamp(Base):
    __tablename__ = "timestamps"

    id = Column(Integer, primary_key=True, unique=True)
    timestamp = Column(Integer)
