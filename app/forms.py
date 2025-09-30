from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from app.models.student import Student

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