from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(10), nullable=False)
    password = Column(String(20), nullable=False)
    ranking = Column(Integer, unique=True)
    speed = Column(Integer)
    accuracy = Column(Float)

    codes = relationship("Code", back_populates="owner")

class Code(Base):
    __tablename__ = "code"

    id = Column(Integer, primary_key=True, autoincrement=True)
    language = Column(String(20), nullable=False)
    code = Column(Text, nullable=False)
    owner_id = Column(Integer, ForeignKey("user.id"))

    owner = relationship("User", back_populates="codes")
