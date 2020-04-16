from sqlalchemy import Column, Integer, String

import sys
sys.path.append("..")

from DB_shell import DB

Base = DB.Base

class Plane(Base):
    __tablename__ = 'plane'
    __table_args__ = {'extend_existing': True}

    plane_id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)