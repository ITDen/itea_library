from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Email, Length, Optional
from database.models import Reader


class SignInForm(FlaskForm):
    """Reader SignIn form"""
    email = StringField('Email', validators=[Email(message='Enter a valid email.'), DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign In')


class SignUpReaderForm(FlaskForm):
    """Reader adding form"""
    name = StringField('Name', validators=[DataRequired()])
    surname = StringField('Surname', validators=[Length(max=64), DataRequired()])
    email = StringField('Email', validators=[Length(min=10), Email(message='Enter a valid email.'), DataRequired()])
    password = PasswordField('Password',
                             validators=[DataRequired(), Length(min=8, message='Select a stronger password.')])
    confirm_password = PasswordField('Confirm password', validators=[Length(min=8)])


class EditReaderForm(FlaskForm):
    """Reader editing form"""
    name = StringField('Name', validators=[DataRequired()])
    surname = StringField('Surname', validators=[Length(max=64), DataRequired()])
    password = PasswordField('New password', validators=[Length(min=8), Optional()])
    confirm_password = PasswordField('Confirm password', validators=[Length(min=8), Optional()])
    email = StringField('Email', validators=[Length(min=10), Email(message='Enter a valid email.'), DataRequired()])
    is_active = BooleanField('Is active')
    is_superuser = BooleanField('Is superuser')


class AddBookForm(FlaskForm):
    """Book adding form"""
    title = StringField('Title', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    year = IntegerField('Year')


class EditBookForm(FlaskForm):
    """Book editing form"""
    title = StringField('Title', validators=[DataRequired()])
    author = StringField('Author', validators=[DataRequired()])
    year = IntegerField('Year')
    reader = QuerySelectField('Reader', query_factory=lambda: Reader.query.all(), allow_blank=True)


class SearchForm(FlaskForm):
    """Search form"""
    query = StringField('Search')
