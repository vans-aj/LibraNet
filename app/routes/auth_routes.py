from flask import render_template, redirect, url_for, flash , request
from datetime import datetime
from decimal import Decimal
from flask import render_template, redirect, url_for, flash, request, session
from datetime import datetime
from decimal import Decimal
from app import db, mail
from app.routes import main_bp
from app.forms import LoginForm, RegistrationForm, OTPVerificationForm
from flask_login import login_user, logout_user, login_required, current_user
from app.models.student import Student
from app.models.loan import Loan
from app.models.fine import Fine
from app.models.otp import OTP
from app.models import FineStatusEnum
from flask_mail import Message

# Helper function to send OTP email
def send_otp_email(email, otp_code):
    """Send OTP verification email."""
    try:
        msg = Message(
            subject='LibraNet - Email Verification OTP',
            recipients=[email]
        )
        msg.html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{
                    font-family: 'Arial', sans-serif;
                    background-color: #f4f4f4;
                    margin: 0;
                    padding: 0;
                }}
                .container {{
                    max-width: 600px;
                    margin: 40px auto;
                    background: white;
                    border-radius: 12px;
                    overflow: hidden;
                    box-shadow: 0 4px 20px rgba(0,0,0,0.1);
                }}
                .header {{
                    background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
                    color: white;
                    padding: 30px;
                    text-align: center;
                }}
                .header h1 {{
                    margin: 0;
                    font-size: 28px;
                }}
                .content {{
                    padding: 40px 30px;
                }}
                .otp-box {{
                    background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
                    border: 2px solid #6366f1;
                    border-radius: 12px;
                    padding: 30px;
                    text-align: center;
                    margin: 30px 0;
                }}
                .otp-code {{
                    font-size: 42px;
                    font-weight: bold;
                    color: #6366f1;
                    letter-spacing: 8px;
                    margin: 10px 0;
                }}
                .warning {{
                    background: #fef3c7;
                    border-left: 4px solid #f59e0b;
                    padding: 15px;
                    margin: 20px 0;
                    border-radius: 4px;
                }}
                .footer {{
                    background: #f8fafc;
                    padding: 20px;
                    text-align: center;
                    color: #64748b;
                    font-size: 14px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>📚 LibraNet</h1>
                    <p style="margin: 10px 0 0;">Email Verification</p>
                </div>
                <div class="content">
                    <h2 style="color: #0f172a;">Welcome to LibraNet!</h2>
                    <p style="color: #64748b; line-height: 1.6;">
                        Thank you for registering with LibraNet. To complete your registration, 
                        please use the following One-Time Password (OTP):
                    </p>
                    
                    <div class="otp-box">
                        <p style="margin: 0; color: #64748b; font-size: 14px;">Your OTP Code</p>
                        <div class="otp-code">{otp_code}</div>
                        <p style="margin: 10px 0 0; color: #64748b; font-size: 14px;">
                            Valid for 10 minutes
                        </p>
                    </div>
                    
                    <div class="warning">
                        <strong>⚠️ Security Notice:</strong>
                        <ul style="margin: 10px 0 0; padding-left: 20px;">
                            <li>Never share this OTP with anyone</li>
                            <li>LibraNet will never ask for your OTP via phone or email</li>
                            <li>This OTP will expire in 10 minutes</li>
                        </ul>
                    </div>
                    
                    <p style="color: #64748b; line-height: 1.6;">
                        If you didn't request this OTP, please ignore this email or contact our support team.
                    </p>
                </div>
                <div class="footer">
                    <p>© 2024 LibraNet. All rights reserved.</p>
                    <p>Graphic Era Hill University</p>
                </div>
            </div>
        </body>
        </html>
        """
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False


@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.list_books'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        # Store registration data in session
        session['registration_data'] = {
            'name': form.name.data,
            'email': form.email.data,
            'roll_no': form.roll_no.data,
            'phone': form.phone.data,
            'password': form.password.data
        }
        
        # Delete any existing OTPs for this email
        OTP.query.filter_by(email=form.email.data).delete()
        
        # Generate and save new OTP
        otp = OTP(email=form.email.data, expiry_minutes=10)
        db.session.add(otp)
        db.session.commit()
        
        # Send OTP email
        if send_otp_email(form.email.data, otp.otp_code):
            flash(f'OTP has been sent to {form.email.data}. Please check your inbox.', 'info')
            return redirect(url_for('main.verify_otp'))
        else:
            flash('Failed to send OTP email. Please try again.', 'danger')
            db.session.delete(otp)
            db.session.commit()
    
    return render_template('register.html', title='Register', form=form)


@main_bp.route('/verify-otp', methods=['GET', 'POST'])
def verify_otp():
    if current_user.is_authenticated:
        return redirect(url_for('main.list_books'))
    
    # Check if registration data exists in session
    if 'registration_data' not in session:
        flash('Please complete the registration form first.', 'warning')
        return redirect(url_for('main.register'))
    
    form = OTPVerificationForm()
    email = session['registration_data']['email']
    
    if form.validate_on_submit():
        # Get the latest valid OTP for this email
        otp_record = OTP.query.filter_by(
            email=email,
            is_used=False
        ).order_by(OTP.created_at.desc()).first()
        
        if not otp_record:
            flash('OTP has expired or is invalid. Please register again.', 'danger')
            session.pop('registration_data', None)
            return redirect(url_for('main.register'))
        
        # Check if OTP is valid
        if not otp_record.is_valid():
            if otp_record.attempts >= 3:
                flash('Too many failed attempts. Please request a new OTP.', 'danger')
                db.session.delete(otp_record)
                db.session.commit()
                session.pop('registration_data', None)
                return redirect(url_for('main.register'))
            else:
                flash('OTP has expired. Please request a new OTP.', 'danger')
                session.pop('registration_data', None)
                return redirect(url_for('main.register'))
        
        # Verify OTP
        if otp_record.otp_code == form.otp.data:
            # OTP is correct - create the user
            reg_data = session['registration_data']
            student = Student(
                name=reg_data['name'],
                email=reg_data['email'],
                roll_no=reg_data['roll_no'],
                phone=reg_data['phone']
            )
            student.set_password(reg_data['password'])
            
            # Mark OTP as used
            otp_record.is_used = True
            
            db.session.add(student)
            db.session.commit()
            
            # Clear session data
            session.pop('registration_data', None)
            
            flash('Email verified successfully! You can now login.', 'success')
            return redirect(url_for('main.login'))
        else:
            # Wrong OTP
            otp_record.attempts += 1
            db.session.commit()
            
            remaining_attempts = 3 - otp_record.attempts
            if remaining_attempts > 0:
                flash(f'Invalid OTP. {remaining_attempts} attempts remaining.', 'danger')
            else:
                flash('Too many failed attempts. Please register again.', 'danger')
                db.session.delete(otp_record)
                db.session.commit()
                session.pop('registration_data', None)
                return redirect(url_for('main.register'))
    
    return render_template('verify_otp.html', title='Verify OTP', form=form, email=email)


@main_bp.route('/resend-otp', methods=['POST'])
def resend_otp():
    if 'registration_data' not in session:
        flash('Session expired. Please register again.', 'warning')
        return redirect(url_for('main.register'))
    
    email = session['registration_data']['email']
    
    # Delete old OTPs
    OTP.query.filter_by(email=email).delete()
    
    # Generate new OTP
    otp = OTP(email=email, expiry_minutes=10)
    db.session.add(otp)
    db.session.commit()
    
    # Send email
    if send_otp_email(email, otp.otp_code):
        flash('New OTP has been sent to your email.', 'success')
    else:
        flash('Failed to send OTP. Please try again.', 'danger')
    
    return redirect(url_for('main.verify_otp'))


@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        student = Student.query.filter_by(email=form.email.data).first()
        
        if student is None or not student.check_password(form.password.data):
            flash('Invalid email or password', 'danger')
            return redirect(url_for('main.login'))
        
        login_user(student, remember=form.remember_me.data)
        flash('You have been logged in successfully!', 'success')

        next_page = request.args.get('next')
        if not next_page or not next_page.startswith('/'):
            next_page = url_for('main.list_books')
        
        return redirect(next_page)
        
    return render_template('login.html', title='Sign In', form=form)


# ... rest of your auth routes remain the same ...



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

    # --- CHANGED: Sync overdue fines (₹500.00 per week) ---
    now_dt = datetime.utcnow()
    fine_rate_per_week = Decimal('500.00') # New rate
    changes_made = False
    
    for loan in loans:
        if loan.returned_date is None and loan.due_date < now_dt:
            days_overdue = (now_dt - loan.due_date).days
            
            if days_overdue > 0:
                # Calculate weeks overdue, rounding up.
                # (1-7 days = 1 week, 8-14 days = 2 weeks, etc.)
                weeks_overdue = (days_overdue - 1) // 7 + 1
                amount_due = fine_rate_per_week * weeks_overdue
            else:
                amount_due = Decimal('0.00')

            if loan.fine is None:
                if amount_due > 0:
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