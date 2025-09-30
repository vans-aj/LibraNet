from flask import render_template, redirect, url_for, flash
from app import db
from app.routes import main_bp  # Import the blueprint from the __init__.py in the same folder
from app.forms import LoginForm, RegistrationForm
from app.models.student import Student

# Note: We use @main_bp.route instead of @app.route
@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        student = Student(
            name=form.name.data,
            email=form.email.data,
            roll_no=form.roll_no.data,
            phone = form.phone.data
        )
        student.set_password(form.password.data)
        db.session.add(student)
        db.session.commit()
        flash('Congratulations, you are now a registered user!', 'success')
        # Note the url_for uses the blueprint name 'main'
        return redirect(url_for('main.login'))
    # The templates are now in the top-level templates folder
    return render_template('register.html', title='Register', form=form)


@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}'.format(form.email.data), 'info')
        # We will add real login logic here later
        return redirect(url_for('main.login'))
    return render_template('login.html', title='Sign In', form=form)