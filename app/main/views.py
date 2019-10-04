from flask import render_template,request,redirect,url_for, abort
from . import main
from .forms import UpdateProfile,BookForm,UpdateForm
from .. import db,photos
from ..models import User,Book,Page
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import markdown2

@main.route('/', methods = ['GET', 'POST'])
def index():
  '''
    View root page function that returns the index page and its data
    '''
 
  title="Home| Welcome to Ebook Maker"
  books = Book.get_books()
  return render_template('index.html',title = title,books = books)


@main.route('/book/new/', methods = ['GET', 'POST'])
@login_required
def add_book():
    form = BookForm()
   
    if form.validate_on_submit():
        title = form.title.data
        image = form.image.data
        filename = photos.save(image)
        print(filename)
        path = f'photos/{filename}'
        content = form.content.data
        new_book = Book(title = title, image = path,content=content)
        new_book.save_book()
         
        return redirect(url_for('.index'))
        
    title = 'Add Book'    
    
    return render_template('book.html', title = title, ola = form)


    #############################
@main.route('/edit/book/<int:id>',methods= ['GET','POST'])
@login_required
def update_page(id):
    book=Book.query.filter_by(id=id).first()
    if book is None:
        abort(404)

    form=UpdateForm()
    user = current_user
    if form.validate_on_submit():
        book.content=form.content.data

        db.session.add(book)
        db.session.commit()

        return redirect(url_for('main.index'))
    elif request.method == 'GET':
        
        book.content =form.content.data
        

    return render_template('update.html',form =form,book=book)    

@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)
@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)
@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))


