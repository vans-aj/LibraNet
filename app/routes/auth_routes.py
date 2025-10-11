from flask import render_template, redirect, url_for, flash , request
from app import db
from app.routes import main_bp  # Import the blueprint from the __init__.py in the same folder
from app.forms import LoginForm, RegistrationForm
from flask_login import login_user, logout_user, login_required, current_user
from app.models.student import Student
from app.models.loan import Loan

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
        # Find the student in the database by their email
        student = Student.query.filter_by(email=form.email.data).first()
        
        # Check if the student exists and if the password is correct
        if student is None or not student.check_password(form.password.data):
            flash('Invalid email or password', 'danger')
            return redirect(url_for('main.list_books'))
        
        # If credentials are correct, log the user in with Flask-Login
        login_user(student, remember=form.remember_me.data)
        flash('You have been logged in successfully!', 'success')

        next_page = request.args.get('next')
        if not next_page or not next_page.startswith('/'):
            next_page = url_for('main.list_books')
        
        # Redirect to the dashboard page after a successful login
        return redirect(next_page)
        
    return render_template('login.html', title='Sign In', form=form)


@main_bp.route('/logout')
def logout():
    """Logs the user out."""
    logout_user() # This function from Flask-Login clears the user's session
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.login'))

@main_bp.route('/my-loans')
@login_required
def my_loans():
    """Displays all the books currently borrowed by the logged-in user."""
    # This query finds all loans associated with the current user.
    # We must now use the .book relationship which points to a PhysicalBook.
    loans = Loan.query.filter_by(student_id=current_user.id).all()
    
    return render_template('my_loans.html', title='My Loans', loans=loans)

@main_bp.route('/profile')
@login_required
def profile():
    """
    Displays the user's profile page.
    """
    return render_template('profile.html', title='My Profile')