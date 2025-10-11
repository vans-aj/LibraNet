from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, Optional, NumberRange
from app.models.student import Student
from app.models.physical_book import PhysicalBook

class RegistrationForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=150)])
    roll_no = StringField('University Roll Number', validators=[DataRequired(), Length(min=4, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match.')])
    phone = StringField('Phone',validators=[Length(min=10,max=10)])
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = Student.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already taken. Please choose a different one.')

    def validate_roll_no(self, roll_no):
        user = Student.query.filter_by(roll_no=roll_no.data).first()
        if user:
            raise ValidationError('That roll number is already registered.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')

class BookForm(FlaskForm):
    """Form for admins to add or edit a book."""
    title = StringField('Title', validators=[DataRequired(), Length(max=200)])
    author = StringField('Author', validators=[DataRequired(), Length(max=150)])
    summary = TextAreaField('Summary')
    isbn = StringField('ISBN', validators=[Optional(), Length(max=20)])
    total_copies = IntegerField('Total Copies', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Submit Book')

    def __init__(self, original_book=None, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)
        self.original_book = original_book

    def validate_isbn(self, isbn):
        if isbn.data:
            book = PhysicalBook.query.filter_by(isbn=isbn.data).first()
            if book and (self.original_book is None or book.id != self.original_book.id):
                raise ValidationError('This ISBN is already registered.')