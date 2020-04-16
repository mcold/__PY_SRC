from sqlalchemy import Column, Integer, String

import sys
sys.path.append("..")

from DB_shell import DB

Base = DB.Base

class Book(Base):
    __tablename__ = 'book'
    __table_args__ = {'extend_existing': True}

    book_id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    summary = Column(String(2000))
    comment = Column(String(3000))