from flask import render_template,request,redirect,url_for, abort
from . import main
from .forms import UpdateProfile
from .. import db,photos
from ..models import Author,Admin
from flask_login import login_required, current_user

@main.route('/', methods = ['GET', 'POST'])
def index():
  '''
    View root page function that returns the index page and its data
    '''
 
  title="Home| Welcome to Ebook Maker"
  
  return render_template('index.html')
