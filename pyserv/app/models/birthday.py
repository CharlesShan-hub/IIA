from sqlalchemy import Column, Integer, String, Date
from app.database.database import Base

class Birthday(Base):
    __tablename__ = "birthdays"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    birthdate = Column(Date)