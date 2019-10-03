from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager
from datetime import datetime
     

class Author(UserMixin,db.Model):
    __tablename__ = 'authors'

    id = db.Column(db.Integer,primary_key = True)
    author_name = db.Column(db.String(255),index = True)
    email = db.Column(db.String(255),unique = True,index = True)
    password_hash = db.Column(db.String(255))
    pass_secure=db.Column(db.String(255))
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    books = db.relationship('Book',backref='authors' ,lazy='dynamic')
    
    @login_manager.user_loader
    def load_user(user_id):
        return Author.query.get(int(user_id))


    
    @property
    def password(self):
            raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
            self.pass_secure = generate_password_hash(password)


    def verify_password(self,password):
            return check_password_hash(self.pass_secure,password)
    
    def __repr__(self):
      return f'Author {self.author_name}'




class Book(UserMixin,db.Model):

    __tablename__ = 'books'

    id = db.Column(db.Integer,primary_key = True)
    book_name=db.Column(db.String)
    content = db.Column(db.String)
    author_id = db.Column(db.Integer,db.ForeignKey('authors.id'))
    page = db.relationship('Page',backref='books' ,lazy='dynamic')
    
    def save_book(self):
        db.session.add(self)
        db.session.commit()
    def update_book(self):
        db.session.add(self)
        db.session.commit()
    @classmethod
    def get_books(cls):
        books = Book.query.all()
        return books

class Page(db.Model):
    __tablename__= 'pages'
    
    id= db.Column(db.Integer,primary_key= True)
    page_number=db.Column(db.Integer)
    book_id = db.Column(db.Integer,db.ForeignKey('books.id'))
    author_id = db.Column(db.Integer,db.ForeignKey('authors.id'))
    def save_page(self):
        db.session.add(self)
        db.session.commit()
    @classmethod
    def get_pages(cls):
        pages = Page.query.all()
        return pages
