from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, SelectField, TextAreaField, FloatField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, Optional, NumberRange, Regexp
from app.models.student import Student
from app.models.physical_book import PhysicalBook
from app.models.ebook import Ebook
from app.models.audiobook import Audiobook

class RegistrationForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=150)])
    roll_no = StringField('University Roll Number', validators=[DataRequired(), Length(min=4, max=64)])
    email = StringField('Email', validators=[
        DataRequired(), 
        Email(),
        Regexp(r'^[a-zA-Z0-9._%+-]+@gehu\.ac\.in$', message='Only @gehu.ac.in email addresses are allowed')
    ])
    phone = StringField('Phone', validators=[Length(min=10, max=10)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(), 
        EqualTo('password', message='Passwords must match.')
    ])
    submit = SubmitField('Send OTP')

    def validate_email(self, email):
        user = Student.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already registered. Please login instead.')

    def validate_roll_no(self, roll_no):
        user = Student.query.filter_by(roll_no=roll_no.data).first()
        if user:
            raise ValidationError('That roll number is already registered.')


class OTPVerificationForm(FlaskForm):
    otp = StringField('Enter OTP', validators=[
        DataRequired(),
        Length(min=6, max=6, message='OTP must be 6 digits'),
        Regexp(r'^\d{6}$', message='OTP must contain only numbers')
    ])
    submit = SubmitField('Verify OTP')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')

# ... rest of your forms remain the same ...

class BookForm(FlaskForm):
    """Form for admins to add or edit a physical book."""
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


class EbookForm(FlaskForm):
    """Form for admins to add or edit an ebook."""
    title = StringField('Title', validators=[DataRequired(), Length(max=200)])
    author = StringField('Author', validators=[DataRequired(), Length(max=150)])
    summary = TextAreaField('Summary')
    file_path = StringField('File Path', validators=[DataRequired(), Length(max=255)])
    file_format = SelectField('File Format', 
                             choices=[('PDF', 'PDF'), ('EPUB', 'EPUB'), ('MOBI', 'MOBI')],
                             validators=[DataRequired()])
    file_size_mb = FloatField('File Size (MB)', validators=[Optional(), NumberRange(min=0)])
    submit = SubmitField('Submit Ebook')


class AudiobookForm(FlaskForm):
    """Form for admins to add or edit an audiobook."""
    title = StringField('Title', validators=[DataRequired(), Length(max=200)])
    author = StringField('Author', validators=[DataRequired(), Length(max=150)])
    narrator = StringField('Narrator', validators=[Optional(), Length(max=150)])
    summary = TextAreaField('Summary')
    file_path = StringField('File Path', validators=[DataRequired(), Length(max=255)])
    duration_minutes = IntegerField('Duration (minutes)', validators=[Optional(), NumberRange(min=1)])
    file_format = SelectField('File Format', 
                             choices=[('MP3', 'MP3'), ('M4B', 'M4B'), ('AAC', 'AAC')],
                             validators=[DataRequired()])
    file_size_mb = FloatField('File Size (MB)', validators=[Optional(), NumberRange(min=0)])
    submit = SubmitField('Submit Audiobook')