from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager
from datetime import datetime
     
class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(255))
    authors = db.relationship('Author',backref = 'role',lazy="dynamic")
    admin = db.relationship('Admin',backref = 'role',lazy="dynamic")
    def save_comment(self):
        db.session.add(self)
        db.session.commit()
    def __repr__(self):
        return f'Author {self.name}'


class Author(UserMixin,db.Model):
    __tablename__ = 'authors'

    id = db.Column(db.Integer,primary_key = True)
    author_name = db.Column(db.String(255),index = True)
    email = db.Column(db.String(255),unique = True,index = True)
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(255))
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    books = db.relationship('Comment',backref='author' ,lazy='dynamic')
    comments = db.relationship('Comment',backref='author' ,lazy='dynamic')
    
    
   
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    
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



class Admin(UserMixin,db.Model):

    __tablename__ = 'admin'

    id = db.Column(db.Integer,primary_key = True)
    username=db.Column(db.String)
    email = db.Column(db.String)
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
    comments = db.relationship('Comment',backref='admin' ,lazy='dynamic')
    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.pass_secure = generate_password_hash(password)


    def verify_password(self,password):
        return check_password_hash(self.pass_secure,password)

    def __repr__(self):
        return f'User {self.username}'

class Book(UserMixin,db.Model):

    __tablename__ = 'books'

    id = db.Column(db.Integer,primary_key = True)
    book_name=db.Column(db.String)
    content = db.Column(db.String)
    page_number=db.Column(db.Integer)
    author_id = db.Column(db.Integer,db.ForeignKey('authors.id'))
    comments = db.relationship('Comment',backref='book' ,lazy='dynamic')
    def save_book(self):
        db.session.add(self)
        db.session.commit()
    def update_book(self):
        db.session.add(self)
        db.session.commit()


class Comment(db.Model):
    __tablename__= 'comments'
    
    id= db.Column(db.Integer,primary_key= True)
    comment=db.Column(db.String(255))
    book_id = db.Column(db.Integer,db.ForeignKey('books.id'))
    author_id = db.Column(db.Integer,db.ForeignKey('authors.id'))
    admin_id = db.Column(db.Integer,db.ForeignKey('admin.id'))
    
    def save_comment(self):
        db.session.add(self)
        db.session.commit()
    @classmethod
    def get_comments(cls,id):
        comments = Comment.query.filter_by(book_id=id).all()
        return comments
    def delete_comment(self):
       db.session.delete(self)
       db.session.commit()
    
