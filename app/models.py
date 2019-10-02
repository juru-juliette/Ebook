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
    def __repr__(self):
        return f'Author {self.name}'


class Author(UserMixin,db.Model):
    __tablename__ = 'authors'

    id = db.Column(db.Integer,primary_key = True)
    authorname = db.Column(db.String(255),index = True)
    email = db.Column(db.String(255),unique = True,index = True)
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
    password_hash = db.Column(db.String(255))
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    
    
    def __repr__(self):
      return f'Author {self.username}'

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


class Admin(UserMixin,db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer,primary_key = True)
    username=db.Column(db.String)
    email = db.Column(db.String)
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))