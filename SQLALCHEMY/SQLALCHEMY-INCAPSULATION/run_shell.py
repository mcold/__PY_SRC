# coding: utf-8

# take all classes from Models -> create in time of initialization
from DB_shell import DB
from Models.Book import Book
from Models.Plane import Plane

db = DB('my_db')


my_book = Book(book_id=1, title='Martin Iden', summary='Super interesting book', comment='my comment')
db.add(my_book)

# my_plane = Plane(plane_id = 1, name='Afrodita')
db.add(my_book)
db.commit()