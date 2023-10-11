from sqlalchemy import Column, Integer, String, SmallInteger

from database import Base


class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(2000), index=True)
    description = Column(String(10000), nullable=True)
    year = Column(SmallInteger, index=True, nullable=True)
