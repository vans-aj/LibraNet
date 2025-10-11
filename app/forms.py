from flask_wtf import FlaskForm
# Make sure to add IntegerField, SelectField to this import
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, SelectField
# Make sure to add Optional and NumberRange to this import
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, Optional, NumberRange
from app.models.student import Student
from app.models.physical_book import PhysicalBook         # <-- Import the Book model

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

# In app/forms.py

# ... (other imports are the same) ...

class BookForm(FlaskForm):
    """Form for admins to add or edit a book."""
    title = StringField('Title', validators=[DataRequired(), Length(max=200)])
    author = StringField('Author', validators=[DataRequired(), Length(max=150)])
    isbn = StringField('ISBN', validators=[Optional(), Length(max=20)])
    total_copies = IntegerField('Total Copies', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Submit Book')

    # --- THIS IS THE NEW PART ---
    def __init__(self, original_book=None, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)
        self.original_book = original_book

    # --- THIS IS THE UPDATED VALIDATOR ---
    def validate_isbn(self, isbn):
        if isbn.data:
            book = PhysicalBook.query.filter_by(isbn=isbn.data).first()
            # If a book is found AND it's a different book from the one we are editing
            if book and (self.original_book is None or book.id != self.original_book.id):
                raise ValidationError('This ISBN is already registered.')