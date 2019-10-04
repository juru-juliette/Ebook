from flask_wtf import FlaskForm
from wtforms.validators import Required
from flask_wtf.file import FileField, FileRequired
from wtforms import ValidationError
from ..models import User
from wtforms import StringField,SelectField,TextAreaField,SubmitField,FileField,IntegerField

class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.',validators = [Required()])
    submit = SubmitField('Submit')
    
class BookForm(FlaskForm):
    title=StringField('Title',validators = [Required()])
    image = FileField('Photo', validators=[FileRequired()])
    content=TextAreaField('Content',validators = [Required()])
    submit=SubmitField('SUBMIT')
class UpdateForm (FlaskForm):
    title=StringField('Title',validators = [Required()])
    content=TextAreaField('Content',validators = [Required()])
    submit=SubmitField('SUBMIT')