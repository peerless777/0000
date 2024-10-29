from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField, ValidationError, BooleanField
from wtforms.validators import data_required, EqualTo, Length
from flask_ckeditor import CKEditorField


# Create A Search Form
class searchform(FlaskForm) :
    searched = StringField("Searched", validators=[data_required()])
    submit = SubmitField("Submit")



# Create Posts Form
class postform(FlaskForm) :
    title = StringField("Title", validators=[data_required()])
    # content = StringField("Content", validators=[data_required()])
    content = CKEditorField("Content", validators=[data_required()])
    author = StringField("Author")
    slug = StringField("Slug", validators=[data_required()])
    submit = SubmitField("Submit")



# Create users Form Class
class usersrform(FlaskForm) :
    name = StringField("Name", validators=[data_required()])
    username = StringField("Username", validators=[data_required()])
    email = StringField("Email", validators=[data_required()])
    favorite_color = StringField("favorite_color")
    password_hash = PasswordField('Password', validators=[data_required(), EqualTo('password_hash2', message='Passwords Must Mach!')])
    password_hash2 = PasswordField('Confirm Password', validators=[data_required()])
    submit = SubmitField("Submit")



# Create Passwd Fomr Class
class passwordform(FlaskForm) :
    email = StringField("What's Your email?", validators=[data_required()])
    password_hash = PasswordField("What's Your password?", validators=[data_required()])
    submit = SubmitField("Submit")



# Create Name Form Class
class namerform(FlaskForm) :
    name = StringField("What's Your Name?", validators=[data_required()])
    submit = SubmitField("Submit")



# Create LoginForm
class loginform(FlaskForm) :
    username = StringField("Username", validators=[data_required()])
    password_hash = PasswordField("Password", validators=[data_required()])
    submit = SubmitField("Submit")
