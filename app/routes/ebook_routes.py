from flask import render_template, flash, redirect, url_for, request, abort, send_file
from flask_login import login_required, current_user
from app.routes import main_bp
from app.models.ebook import Ebook
from app import db
from sqlalchemy import or_
import os

@main_bp.route('/ebooks')
@login_required
def list_ebooks():
    """Display list of ebooks."""
    # Check subscription access
    if not current_user.has_access_to_ebooks():
        flash('You need a Pro or Max subscription to access ebooks.', 'warning')
        return redirect(url_for('main.subscriptions'))
    
    search_term = request.args.get('q', '', type=str)
    
    if search_term:
        ebooks = Ebook.query.filter(
            or_(
                Ebook.title.ilike(f'%{search_term}%'),
                Ebook.author.ilike(f'%{search_term}%')
            )
        ).order_by(Ebook.title).all()
    else:
        ebooks = Ebook.query.order_by(Ebook.title).all()
    
    return render_template(
        'ebooks/list.html',
        title='Ebooks Collection',
        ebooks=ebooks,
        search_term=search_term
    )


@main_bp.route('/ebook/<int:ebook_id>')
@login_required
def ebook_detail(ebook_id):
    """Display ebook details."""
    # Check subscription access
    if not current_user.has_access_to_ebooks():
        flash('You need a Pro or Max subscription to access ebooks.', 'warning')
        return redirect(url_for('main.subscriptions'))
    
    ebook = Ebook.query.get_or_404(ebook_id)
    
    return render_template(
        'ebooks/detail.html',
        title=ebook.title,
        ebook=ebook
    )


@main_bp.route('/ebook/<int:ebook_id>/read')
@login_required
def read_ebook(ebook_id):
    """Read/view ebook."""
    # Check subscription access
    if not current_user.has_access_to_ebooks():
        flash('You need a Pro or Max subscription to access ebooks.', 'warning')
        return redirect(url_for('main.subscriptions'))
    
    ebook = Ebook.query.get_or_404(ebook_id)
    
    return render_template(
        'ebooks/reader.html',
        title=f'Reading: {ebook.title}',
        ebook=ebook
    )


@main_bp.route('/ebook/<int:ebook_id>/download')
@login_required
def download_ebook(ebook_id):
    """Download ebook file."""
    # Check subscription access
    if not current_user.has_access_to_ebooks():
        flash('You need a Pro or Max subscription to download ebooks.', 'warning')
        return redirect(url_for('main.subscriptions'))
    
    ebook = Ebook.query.get_or_404(ebook_id)
    
    # In production, this would serve the actual file
    # For now, just show a message
    flash(f'Downloading {ebook.title}...', 'info')
    return redirect(url_for('main.ebook_detail', ebook_id=ebook_id))