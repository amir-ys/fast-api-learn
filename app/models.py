from sqlalchemy import Column, Integer, String
from app.database import Base

class Fact(Base):
    __tablename__ = "facts"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)
