from flask import render_template, redirect, url_for, flash , request
from datetime import datetime
from decimal import Decimal
from app import db
from app.routes import main_bp  # Import the blueprint from the __init__.py in the same folder
from app.forms import LoginForm, RegistrationForm
from flask_login import login_user, logout_user, login_required, current_user
from app.models.student import Student
from app.models.loan import Loan
from app.models.fine import Fine
from app.models import FineStatusEnum

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

    # Sync overdue fines (simple rule: 2.00 per overdue day)
    now_dt = datetime.utcnow()
    fine_rate_per_day = Decimal('2.00')
    changes_made = False
    for loan in loans:
        if loan.returned_date is None and loan.due_date < now_dt:
            days_overdue = max((now_dt - loan.due_date).days, 1)
            amount_due = fine_rate_per_day * days_overdue
            if loan.fine is None:
                db.session.add(Fine(amount=amount_due, loan=loan))
                changes_made = True
            else:
                if loan.fine.status == FineStatusEnum.PENDING and loan.fine.amount != amount_due:
                    loan.fine.amount = amount_due
                    changes_made = True
        else:
            # If no longer overdue and a pending fine exists with zero balance, mark paid
            if loan.fine and loan.fine.status == FineStatusEnum.PENDING and loan.fine.balance <= 0:
                loan.fine.status = FineStatusEnum.PAID
                changes_made = True

    if changes_made:
        db.session.commit()

    return render_template('my_loans.html', title='My Loans', loans=loans, now=now_dt)


@main_bp.route('/dues')
@login_required
def dues():
    """Show current user's fines/dues."""
    fines = (
        Fine.query
        .join(Loan)
        .filter(Loan.student_id == current_user.id)
        .order_by(Fine.issued_date.desc())
        .all()
    )
    return render_template('dues.html', title='My Dues', fines=fines)


@main_bp.route('/pay_fine/<int:fine_id>', methods=['POST'])
@login_required
def pay_fine(fine_id: int):
    """Mark a fine as paid (mock payment)."""
    fine = Fine.query.get_or_404(fine_id)
    # Authorization: ensure fine belongs to current user
    if fine.loan.student_id != current_user.id:
        flash('You are not authorized to pay this fine.', 'danger')
        return redirect(url_for('main.dues'))

    if fine.status == FineStatusEnum.PAID:
        flash('This fine is already paid.', 'info')
        return redirect(url_for('main.dues'))

    # Mock payment: settle full outstanding balance
    fine.paid_amount = fine.amount
    fine.status = FineStatusEnum.PAID
    db.session.commit()
    flash('Payment successful. Your fine has been marked as paid.', 'success')
    return redirect(url_for('main.dues'))

@main_bp.route('/profile')
@login_required
def profile():
    """
    Displays the user's profile page.
    """
    return render_template('profile.html', title='My Profile')