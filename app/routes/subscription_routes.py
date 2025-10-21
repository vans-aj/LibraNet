# ========================================
# FILE: app/routes/subscription_routes.py
# ========================================
from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app.routes import main_bp
from app.models.subscription import Subscription
from app.models import SubscriptionTierEnum
from app import db
from datetime import datetime, timedelta
from decimal import Decimal
import razorpay
import os
import hmac
import hashlib

# Initialize Razorpay Client
RAZORPAY_KEY_ID = os.environ.get('RAZORPAY_KEY_ID', 'rzp_test_YOUR_KEY_ID')
RAZORPAY_KEY_SECRET = os.environ.get('RAZORPAY_KEY_SECRET', 'YOUR_KEY_SECRET')

razorpay_client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))

# Subscription pricing (inclusive of GST)
SUBSCRIPTION_PRICES = {
    SubscriptionTierEnum.FREE: 0,
    SubscriptionTierEnum.BASIC: 49,
    SubscriptionTierEnum.PRO: 150,
    SubscriptionTierEnum.MAX: 300
}

SUBSCRIPTION_FEATURES = {
    SubscriptionTierEnum.FREE: {
        'name': 'Free',
        'price': 0,
        'duration_days': None,
        'features': [
            'Browse book catalog',
            'View book details',
            'Basic search functionality',
            'Access to book summaries'
        ],
        'restrictions': [
            'Cannot borrow physical books',
            'No access to ebooks',
            'No access to audiobooks'
        ]
    },
    SubscriptionTierEnum.BASIC: {
        'name': 'Basic',
        'price': 49,
        'duration_days': 182,
        'features': [
            'All Free features',
            'Borrow up to 5 physical books',
            '6-month loan period',
            'Email notifications',
            'Priority support'
        ],
        'restrictions': [
            'No access to ebooks',
            'No access to audiobooks'
        ]
    },
    SubscriptionTierEnum.PRO: {
        'name': 'Pro',
        'price': 150,
        'duration_days': 182,
        'features': [
            'All Basic features',
            'Access to all ebooks',
            'Unlimited ebook downloads',
            'Offline reading support',
            'No physical book limits',
            'Priority customer support',
            'Early access to new releases'
        ],
        'restrictions': [
            'No access to audiobooks'
        ]
    },
    SubscriptionTierEnum.MAX: {
        'name': 'Max',
        'price': 300,
        'duration_days': 182,
        'features': [
            'All Pro features',
            'Access to all audiobooks',
            'Unlimited streaming',
            'Offline listening',
            'Multiple device sync',
            '24/7 Premium support',
            'Exclusive content access',
            'Ad-free experience'
        ],
        'restrictions': []
    }
}


@main_bp.route('/subscriptions')
@login_required
def subscriptions():
    """Display subscription plans."""
    current_sub = current_user.current_subscription
    return render_template(
        'subscriptions.html',
        title='Subscription Plans',
        plans=SUBSCRIPTION_FEATURES,
        current_subscription=current_sub,
        SubscriptionTierEnum=SubscriptionTierEnum
    )


@main_bp.route('/subscribe/<tier>', methods=['GET', 'POST'])
@login_required
def subscribe(tier):
    """Handle subscription purchase."""
    try:
        tier_enum = SubscriptionTierEnum[tier.upper()]
    except KeyError:
        flash('Invalid subscription tier.', 'danger')
        return redirect(url_for('main.subscriptions'))
    
    # Cannot subscribe to FREE
    if tier_enum == SubscriptionTierEnum.FREE:
        flash('Free tier is automatically assigned.', 'info')
        return redirect(url_for('main.subscriptions'))
    
    current_sub = current_user.current_subscription
    
    # Check if already subscribed to this tier
    if current_sub and current_sub.tier == tier_enum and not current_sub.is_expired:
        flash(f'You are already subscribed to {tier_enum.value.title()} plan.', 'info')
        return redirect(url_for('main.subscriptions'))
    
    if request.method == 'GET':
        # Show confirmation page
        plan_info = SUBSCRIPTION_FEATURES[tier_enum]
        return render_template(
            'subscribe_confirm.html',
            title=f'Subscribe to {plan_info["name"]}',
            plan=plan_info,
            tier=tier_enum,
            razorpay_key_id=RAZORPAY_KEY_ID
        )
    
    # POST method is deprecated - payment now handled via Razorpay
    flash('Please use the secure payment button to complete your subscription.', 'info')
    return redirect(url_for('main.subscribe', tier=tier))


@main_bp.route('/verify_payment', methods=['POST'])
@login_required
def verify_payment():
    """Verify Razorpay payment and activate subscription."""
    try:
        data = request.get_json()
        
        # Extract payment details
        payment_id = data.get('razorpay_payment_id')
        order_id = data.get('razorpay_order_id')
        signature = data.get('razorpay_signature')
        tier = data.get('tier')
        
        # Get tier enum
        try:
            tier_enum = SubscriptionTierEnum[tier.upper()]
        except KeyError:
            return jsonify({'success': False, 'message': 'Invalid tier'}), 400
        
        # Fetch payment details from Razorpay
        try:
            payment = razorpay_client.payment.fetch(payment_id)
            
            # Check if payment is captured
            if payment['status'] != 'captured':
                return jsonify({'success': False, 'message': 'Payment not captured'}), 400
            
        except Exception as e:
            print(f"Razorpay error: {str(e)}")
            return jsonify({'success': False, 'message': 'Payment verification failed'}), 400
        
        # ==================================
        # HERE IS THE FIX (Bug 1)
        # Deactivate ALL currently active subscriptions for this user
        # This handles both None and existing 'FREE' subscriptions correctly.
        # ==================================
        Subscription.query.filter_by(
            student_id=current_user.id, 
            is_active=True
        ).update({'is_active': False})

        
        # Create new subscription
        price = Decimal(str(SUBSCRIPTION_PRICES[tier_enum]))
        duration = SUBSCRIPTION_FEATURES[tier_enum]['duration_days']
        
        new_sub = Subscription(
            student_id=current_user.id,
            tier=tier_enum,
            start_date=datetime.utcnow(),
            end_date=datetime.utcnow() + timedelta(days=duration),
            is_active=True,
            price_paid=price
        )
        
        db.session.add(new_sub)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'subscription_id': new_sub.id,
            'message': 'Subscription activated successfully'
        })
        
    except Exception as e:
        print(f"Error in verify_payment: {str(e)}")
        db.session.rollback()
        return jsonify({'success': False, 'message': 'Server error'}), 500


@main_bp.route('/subscription/success/<int:subscription_id>')
@login_required
def subscription_success(subscription_id):
    """Display subscription success page."""
    subscription = Subscription.query.get_or_404(subscription_id)
    
    # Check ownership
    if subscription.student_id != current_user.id:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('main.subscriptions'))
    
    plan_info = SUBSCRIPTION_FEATURES[subscription.tier]
    
    return render_template(
        'subscription_success.html',
        title='Subscription Successful',
        subscription=subscription,
        plan=plan_info
    )


@main_bp.route('/subscription/cancel', methods=['POST'])
@login_required
def cancel_subscription():
    """Cancel current subscription."""
    current_sub = current_user.current_subscription
    
    if not current_sub or current_sub.tier == SubscriptionTierEnum.FREE:
        flash('Cannot cancel free subscription.', 'warning')
        return redirect(url_for('main.subscriptions'))
    
    # Deactivate current subscription
    current_sub.is_active = False
    current_sub.auto_renew = False
    
    # Create FREE subscription
    free_sub = Subscription(
        student_id=current_user.id,
        tier=SubscriptionTierEnum.FREE,
        is_active=True
    )
    
    db.session.add(free_sub)
    db.session.commit()
    
    flash('Subscription cancelled successfully. You are now on the Free plan.', 'success')
    return redirect(url_for('main.subscriptions'))


@main_bp.route('/my-subscription')
@login_required
def my_subscription():
    """View current subscription details."""
    # ==================================
    # HERE IS THE FIX (Bug 2)
    # 1. Get the current subscription object (which might be None)
    # 2. Get the tier *enum* (which defaults to FREE, thanks to your Student model)
    # 3. Get the plan_info dict using the tier enum
    # ==================================
    current_sub = current_user.current_subscription
    current_tier_enum = current_user.subscription_tier
    plan_info = SUBSCRIPTION_FEATURES[current_tier_enum]
    
    # Get subscription history
    all_subs = Subscription.query.filter_by(student_id=current_user.id).order_by(Subscription.start_date.desc()).all()
    
    # If the user is new and has no subscription object yet, create a
    # temporary one just for display on this page (don't save to DB)
    if not current_sub:
        current_sub = Subscription(
            student_id=current_user.id,
            tier=SubscriptionTierEnum.FREE,
            is_active=True
        )

    return render_template(
        'my_subscription.html',
        title='My Subscription',
        subscription=current_sub,
        plan=plan_info, # 'plan' is now guaranteed to be the correct dictionary
        subscription_history=all_subs
    )