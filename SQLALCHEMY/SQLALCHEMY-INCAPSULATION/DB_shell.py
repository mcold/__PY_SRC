from os import curdir
from os.path import join, abspath

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class DB:
	Base = declarative_base()

	def make_session(self):
		Session = sessionmaker(bind=self.engine)
		Session.configure(bind=self.engine)
		self.session = Session()
	def __init__(self, db_name):
		self.db_name = db_name + '.db'
		self.db_path = 'sqlite:///' + join(abspath(curdir), self.db_name)
		self.engine = create_engine(self.db_path)
		self.Base.metadata.create_all(self.engine)
		self.make_session()

	def add(self, obj):
		self.session.add(obj)

	def commit(self):
		self.session.commit()

from Models import *