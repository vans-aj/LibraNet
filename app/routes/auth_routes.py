from flask import render_template, redirect, url_for, flash, request, session, jsonify
from datetime import datetime
from decimal import Decimal
from app import db, mail
from app.routes import main_bp
from app.forms import LoginForm, RegistrationForm, OTPVerificationForm, ForgotPasswordForm, ResetPasswordForm, UpdateProfileForm
from flask_login import login_user, logout_user, login_required, current_user
from app.models.user import User
from app.models.loan import Loan
from app.models.fine import Fine
from app.models.otp import OTP
from app.models import FineStatusEnum
from flask_mail import Message # type: ignore
from google.oauth2 import id_token # type: ignore
from google.auth.transport import requests as google_requests # type: ignore
from flask import current_app
import secrets
from threading import Thread
import requests

from threading import Thread

# Helper function to send emails asynchronously
def send_async_email(app, msg):
    """Send email in background thread."""
    with app.app_context():
        try:
            mail.send(msg)
            print(f"✓ Email sent successfully to {msg.recipients}")
        except Exception as e:
            print(f"✗ Failed to send email: {str(e)}")

# Helper function to send OTP email
def send_otp_email(email, otp_code):
    """Send OTP verification email asynchronously."""
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
                    font-weight: 700;
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
                    <h1>LibraNet</h1>
                    <p style="margin: 10px 0 0; font-size: 16px;">Email Verification</p>
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
        # Send email asynchronously in background
        Thread(target=send_async_email, args=(current_app._get_current_object(), msg)).start()
        return True
    except Exception as e:
        print(f"Error preparing email: {str(e)}")
        return False


@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.list_books'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        # Generate a unique roll number and default name from email
        roll_no = f"LIB-{secrets.token_hex(4).upper()}"
        email_username = form.email.data.split('@')[0]
        
        # Store registration data in session for OTP verification
        session['registration_data'] = {
            'email': form.email.data,
            'password': form.password.data,
            'name': email_username.capitalize(),
            'roll_no': roll_no
        }
        
        # Delete any existing OTPs for this email
        OTP.query.filter_by(email=form.email.data).delete()
        
        # Generate and save new OTP
        otp = OTP(email=form.email.data, expiry_minutes=10)
        db.session.add(otp)
        db.session.commit()
        
        # Send OTP email
        if send_otp_email(form.email.data, otp.otp_code):
            flash(f'Verification code has been sent to {form.email.data}. Please check your inbox.', 'info')
            return redirect(url_for('main.verify_otp'))
        else:
            flash('Failed to send verification email. Please try again.', 'danger')
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
            student = User(
                name=reg_data['name'],
                email=reg_data['email'],
                roll_no=reg_data['roll_no'],
                phone='',
                is_verified=True  # Mark as verified since OTP was successful
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
        student = User.query.filter_by(email=form.email.data).first()
        
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



@main_bp.route('/logout/confirm')
@login_required
def logout_confirm():
    """Display logout confirmation page."""
    return render_template('logout_confirm.html', title='Confirm Logout')

@main_bp.route('/logout')
@login_required
def logout():
    """Logs the user out."""
    logout_user()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('main.landing_page'))


@main_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    """Handle forgot password requests."""
    if current_user.is_authenticated:
        return redirect(url_for('main.books'))
    
    form = ForgotPasswordForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        
        if user:
            # Generate password reset token
            token = secrets.token_urlsafe(32)
            
            # Store token in session with expiry (10 minutes)
            session['reset_token'] = {
                'token': token,
                'email': user.email,
                'created_at': datetime.now().isoformat()
            }
            
            # Send password reset email
            msg = Message(
                subject='LibraNet - Password Reset Request',
                recipients=[user.email]
            )
            
            reset_url = url_for('main.reset_password', token=token, _external=True)
            
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
                        margin: 50px auto;
                        background-color: #ffffff;
                        border-radius: 10px;
                        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                        overflow: hidden;
                    }}
                    .header {{
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        color: white;
                        padding: 30px;
                        text-align: center;
                    }}
                    .header h1 {{
                        margin: 0;
                        font-size: 28px;
                        font-weight: 600;
                    }}
                    .content {{
                        padding: 40px 30px;
                    }}
                    .content p {{
                        color: #333;
                        line-height: 1.6;
                        margin: 15px 0;
                    }}
                    .reset-button {{
                        display: inline-block;
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        color: white;
                        text-decoration: none;
                        padding: 15px 40px;
                        border-radius: 5px;
                        margin: 20px 0;
                        font-weight: 600;
                        text-align: center;
                    }}
                    .reset-button:hover {{
                        opacity: 0.9;
                    }}
                    .footer {{
                        background-color: #f8f9fa;
                        padding: 20px;
                        text-align: center;
                        color: #666;
                        font-size: 12px;
                    }}
                    .warning {{
                        background-color: #fff3cd;
                        border-left: 4px solid #ffc107;
                        padding: 15px;
                        margin: 20px 0;
                        color: #856404;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>📚 LibraNet</h1>
                        <p style="margin: 10px 0 0 0; opacity: 0.9;">Password Reset Request</p>
                    </div>
                    <div class="content">
                        <p>Hello {user.name},</p>
                        <p>We received a request to reset your password. Click the button below to set a new password:</p>
                        
                        <div style="text-align: center;">
                            <a href="{reset_url}" class="reset-button">Reset Password</a>
                        </div>
                        
                        <div class="warning">
                            <strong>⚠️ Important:</strong> This link will expire in 10 minutes.
                        </div>
                        
                        <p>If you didn't request a password reset, you can safely ignore this email. Your password will remain unchanged.</p>
                        
                        <p>If the button doesn't work, copy and paste this link into your browser:</p>
                        <p style="word-break: break-all; color: #667eea;">{reset_url}</p>
                    </div>
                    <div class="footer">
                        <p>© 2024 LibraNet. All rights reserved.</p>
                        <p>This is an automated email. Please do not reply.</p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            # Send email in background thread
            app = current_app._get_current_object()
            Thread(target=send_async_email, args=(app, msg)).start()
            
            flash('Password reset link has been sent to your email.', 'success')
        else:
            # Don't reveal if email exists for security
            flash('If that email is registered, a password reset link has been sent.', 'info')
        
        return redirect(url_for('main.login'))
    
    return render_template('forgot_password.html', title='Forgot Password', form=form)


@main_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """Handle password reset with token."""
    if current_user.is_authenticated:
        return redirect(url_for('main.books'))
    
    # Verify token from session
    reset_data = session.get('reset_token')
    
    if not reset_data or reset_data.get('token') != token:
        flash('Invalid or expired password reset link.', 'danger')
        return redirect(url_for('main.forgot_password'))
    
    # Check if token is expired (10 minutes)
    created_at = datetime.fromisoformat(reset_data['created_at'])
    if (datetime.now() - created_at).total_seconds() > 600:  # 10 minutes
        session.pop('reset_token', None)
        flash('Password reset link has expired. Please request a new one.', 'warning')
        return redirect(url_for('main.forgot_password'))
    
    form = ResetPasswordForm()
    
    if form.validate_on_submit():
        # Find user and update password
        user = User.query.filter_by(email=reset_data['email']).first()
        
        if user:
            user.set_password(form.password.data)
            db.session.commit()
            
            # Clear reset token from session
            session.pop('reset_token', None)
            
            flash('Your password has been reset successfully. You can now login.', 'success')
            return redirect(url_for('main.login'))
        else:
            flash('User not found. Please try again.', 'danger')
            return redirect(url_for('main.forgot_password'))
    
    return render_template('reset_password.html', title='Reset Password', form=form, token=token)


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

@main_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """
    Displays and handles editing of the user's profile page.
    """
    form = UpdateProfileForm()
    
    if form.validate_on_submit():
        # Verify current password
        if not current_user.check_password(form.current_password.data):
            flash('Incorrect password. Please try again.', 'danger')
            return render_template('profile.html', title='My Profile', form=form)
        
        # Check if email is already taken by another user
        if form.email.data != current_user.email:
            existing_user = User.query.filter_by(email=form.email.data).first()
            if existing_user:
                flash('That email is already in use. Please choose a different one.', 'danger')
                return render_template('profile.html', title='My Profile', form=form)
        
        # Update user information
        current_user.name = form.name.data
        current_user.email = form.email.data
        current_user.phone = form.phone.data
        
        try:
            db.session.commit()
            flash('Your profile has been updated successfully!', 'success')
            return redirect(url_for('main.profile'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while updating your profile. Please try again.', 'danger')
            return render_template('profile.html', title='My Profile', form=form)
    
    # Pre-fill form with current user data on GET request
    if request.method == 'GET':
        form.name.data = current_user.name
        form.email.data = current_user.email
        form.phone.data = current_user.phone
    
    return render_template('profile.html', title='My Profile', form=form)

# Google OAuth Routes
@main_bp.route('/auth/google', methods=['POST'])
def google_login():
    """Handle Google Sign-In token verification"""
    try:
        token = request.json.get('credential')
        
        if not token:
            return {'error': 'No token provided'}, 400
        
        # Verify the token with Google
        idinfo = id_token.verify_oauth2_token(
            token, 
            google_requests.Request(), 
            current_app.config['GOOGLE_OAUTH_CLIENT_ID']
        )
        
        # Get user info from token
        email = idinfo.get('email')
        name = idinfo.get('name')
        google_id = idinfo.get('sub')
        
        if not email:
            return {'error': 'Email not provided by Google'}, 400
        
        # Check if user already exists
        student = User.query.filter_by(email=email).first()
        
        if student:
            # User exists, just log them in
            login_user(student, remember=True)
            return {'success': True, 'redirect': url_for('main.list_books')}, 200
        else:
            # New user - create account
            # Generate a random roll number for Google sign-ups
            roll_no = f"GOOGLE-{secrets.token_hex(4).upper()}"
            
            # Create new student account
            new_student = User(
                name=name or email.split('@')[0],
                email=email,
                roll_no=roll_no,
                phone='',  # Optional, can be updated later
                is_verified=True  # Google email is already verified
            )
            
            # Set a random password (user won't need it with OAuth)
            new_student.set_password(secrets.token_urlsafe(32))
            
            db.session.add(new_student)
            db.session.commit()
            
            # Log in the new user
            login_user(new_student, remember=True)
            
            flash(f'Welcome to LibraNet, {name}! Your account has been created.', 'success')
            return {'success': True, 'redirect': url_for('main.list_books')}, 200
            
    except ValueError as e:
        # Invalid token
        return {'error': 'Invalid token'}, 400
    except Exception as e:
        # Other errors
        return {'error': str(e)}, 500


# GitHub OAuth Routes
@main_bp.route('/auth/github')
def github_login():
    """Initiate GitHub OAuth flow"""
    github_client_id = current_app.config.get('GITHUB_OAUTH_CLIENT_ID')
    
    if not github_client_id:
        flash('GitHub authentication is not configured.', 'danger')
        return redirect(url_for('main.login'))
    
    # Store the next URL in session
    session['oauth_next'] = request.args.get('next', url_for('main.list_books'))
    
    # Force localhost callback URL
    callback_url = 'http://localhost:8080/auth/github/callback'
    
    # Redirect to GitHub authorization page
    github_auth_url = (
        f"https://github.com/login/oauth/authorize"
        f"?client_id={github_client_id}"
        f"&redirect_uri={callback_url}"
        f"&scope=user:email"
    )
    
    return redirect(github_auth_url)


@main_bp.route('/auth/github/callback')
def github_callback():
    """Handle GitHub OAuth callback"""
    try:
        code = request.args.get('code')
        
        if not code:
            flash('GitHub authentication failed: No authorization code received.', 'danger')
            return redirect(url_for('main.login'))
        
        github_client_id = current_app.config.get('GITHUB_OAUTH_CLIENT_ID')
        github_client_secret = current_app.config.get('GITHUB_OAUTH_CLIENT_SECRET')
        
        # Force localhost callback URL (must match what was sent to GitHub)
        callback_url = 'http://localhost:8080/auth/github/callback'
        
        # Exchange code for access token
        token_response = requests.post(
            'https://github.com/login/oauth/access_token',
            headers={'Accept': 'application/json'},
            data={
                'client_id': github_client_id,
                'client_secret': github_client_secret,
                'code': code,
                'redirect_uri': callback_url
            }
        )
        
        token_data = token_response.json()
        access_token = token_data.get('access_token')
        
        if not access_token:
            flash('GitHub authentication failed: Could not obtain access token.', 'danger')
            return redirect(url_for('main.login'))
        
        # Get user info from GitHub
        user_response = requests.get(
            'https://api.github.com/user',
            headers={
                'Authorization': f'Bearer {access_token}',
                'Accept': 'application/json'
            }
        )
        
        user_data = user_response.json()
        
        # Get user email if not in primary response
        email = user_data.get('email')
        
        if not email:
            # Fetch user's emails
            email_response = requests.get(
                'https://api.github.com/user/emails',
                headers={
                    'Authorization': f'Bearer {access_token}',
                    'Accept': 'application/json'
                }
            )
            
            emails = email_response.json()
            
            # Find primary verified email
            for email_obj in emails:
                if email_obj.get('primary') and email_obj.get('verified'):
                    email = email_obj.get('email')
                    break
            
            # If no primary, get first verified email
            if not email:
                for email_obj in emails:
                    if email_obj.get('verified'):
                        email = email_obj.get('email')
                        break
        
        if not email:
            flash('GitHub authentication failed: No verified email found. Please add a verified email to your GitHub account.', 'danger')
            return redirect(url_for('main.login'))
        
        name = user_data.get('name') or user_data.get('login')
        github_id = str(user_data.get('id'))
        
        # Check if user already exists
        student = User.query.filter_by(email=email).first()
        
        if student:
            # User exists, just log them in
            login_user(student, remember=True)
            flash(f'Welcome back, {student.name}!', 'success')
        else:
            # New user - create account
            roll_no = f"GITHUB-{secrets.token_hex(4).upper()}"
            
            new_student = User(
                name=name or email.split('@')[0],
                email=email,
                roll_no=roll_no,
                phone='',  # Optional, can be updated later
                is_verified=True  # GitHub email is already verified
            )
            
            # Set a random password (user won't need it with OAuth)
            new_student.set_password(secrets.token_urlsafe(32))
            
            db.session.add(new_student)
            db.session.commit()
            
            # Log in the new user
            login_user(new_student, remember=True)
            
            flash(f'Welcome to LibraNet, {name}! Your account has been created via GitHub.', 'success')
        
        # Redirect to next page or default
        next_page = session.pop('oauth_next', url_for('main.list_books'))
        return redirect(next_page)
        
    except Exception as e:
        print(f"GitHub OAuth error: {str(e)}")
        flash(f'GitHub authentication failed: {str(e)}', 'danger')
        return redirect(url_for('main.login'))
