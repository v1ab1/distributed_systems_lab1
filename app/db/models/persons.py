from sqlalchemy import (
    Column,
    String,
    Integer,
)

from app.db.base import Base


class PersonsDB(Base):
    __tablename__ = "persons"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    age = Column(Integer)
    address = Column(String)
    work = Column(String)
