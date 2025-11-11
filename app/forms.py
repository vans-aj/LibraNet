from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, SelectField, TextAreaField, FloatField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, Optional, NumberRange, Regexp
from app.models.user import User
from app.models.physical_book import PhysicalBook
from app.models.ebook import Ebook
from app.models.audiobook import Audiobook

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(), 
        Email()
    ])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(), 
        EqualTo('password', message='Passwords must match.')
    ])
    submit = SubmitField('Create Account')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is already registered. Please login instead.')


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


class ForgotPasswordForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Send Reset Link')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('New Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm New Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match.')
    ])
    submit = SubmitField('Reset Password')


class UpdateProfileForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(max=150)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[
        Optional(),
        Length(max=20),
        Regexp(r'^[\d\s\-\+\(\)]+$', message='Please enter a valid phone number')
    ])
    current_password = PasswordField('Current Password (required to save changes)', validators=[DataRequired()])
    submit = SubmitField('Save Changes')


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