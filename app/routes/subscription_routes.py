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

# Subscription pricing
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
            'Basic search functionality'
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
        'duration_days': 30,
        'features': [
            'All Free features',
            'Borrow up to 5 physical books',
            'Extended loan periods',
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
        'duration_days': 30,
        'features': [
            'All Basic features',
            'Access to all ebooks',
            'Unlimited downloads',
            'Offline reading',
            'Priority customer support'
        ],
        'restrictions': [
            'No access to audiobooks'
        ]
    },
    SubscriptionTierEnum.MAX: {
        'name': 'Max',
        'price': 300,
        'duration_days': 30,
        'features': [
            'All Pro features',
            'Access to all audiobooks',
            'Unlimited streaming',
            'Offline listening',
            '24/7 Premium support',
            'Early access to new releases'
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
    if current_sub.tier == tier_enum and not current_sub.is_expired:
        flash(f'You are already subscribed to {tier_enum.value.title()} plan.', 'info')
        return redirect(url_for('main.subscriptions'))
    
    if request.method == 'GET':
        # Show confirmation page
        plan_info = SUBSCRIPTION_FEATURES[tier_enum]
        return render_template(
            'subscribe_confirm.html',
            title=f'Subscribe to {plan_info["name"]}',
            plan=plan_info,
            tier=tier_enum
        )
    
    # POST - Process subscription
    # Deactivate current subscription if not FREE
    if current_sub.tier != SubscriptionTierEnum.FREE:
        current_sub.is_active = False
    
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
    
    flash(f'Successfully subscribed to {tier_enum.value.title()} plan!', 'success')
    return redirect(url_for('main.subscription_success', subscription_id=new_sub.id))


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
    
    if current_sub.tier == SubscriptionTierEnum.FREE:
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
    current_sub = current_user.current_subscription
    plan_info = SUBSCRIPTION_FEATURES[current_sub.tier]
    
    # Get subscription history
    all_subs = Subscription.query.filter_by(student_id=current_user.id).order_by(Subscription.start_date.desc()).all()
    
    return render_template(
        'my_subscription.html',
        title='My Subscription',
        subscription=current_sub,
        plan=plan_info,
        subscription_history=all_subs
    )