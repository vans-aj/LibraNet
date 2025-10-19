from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import login_required, current_user
from app.routes import main_bp
from app.models.audiobook import Audiobook
from app import db
from sqlalchemy import or_

@main_bp.route('/audiobooks')
@login_required
def list_audiobooks():
    """Display list of audiobooks."""
    # Check subscription access
    if not current_user.has_access_to_audiobooks():
        flash('You need a Max subscription to access audiobooks.', 'warning')
        return redirect(url_for('main.subscriptions'))
    
    search_term = request.args.get('q', '', type=str)
    
    if search_term:
        audiobooks = Audiobook.query.filter(
            or_(
                Audiobook.title.ilike(f'%{search_term}%'),
                Audiobook.author.ilike(f'%{search_term}%'),
                Audiobook.narrator.ilike(f'%{search_term}%')
            )
        ).order_by(Audiobook.title).all()
    else:
        audiobooks = Audiobook.query.order_by(Audiobook.title).all()
    
    return render_template(
        'audiobooks/list.html',
        title='Audiobooks Collection',
        audiobooks=audiobooks,
        search_term=search_term
    )


@main_bp.route('/audiobook/<int:audiobook_id>')
@login_required
def audiobook_detail(audiobook_id):
    """Display audiobook details."""
    # Check subscription access
    if not current_user.has_access_to_audiobooks():
        flash('You need a Max subscription to access audiobooks.', 'warning')
        return redirect(url_for('main.subscriptions'))
    
    audiobook = Audiobook.query.get_or_404(audiobook_id)
    
    return render_template(
        'audiobooks/detail.html',
        title=audiobook.title,
        audiobook=audiobook
    )


@main_bp.route('/audiobook/<int:audiobook_id>/listen')
@login_required
def listen_audiobook(audiobook_id):
    """Listen to audiobook."""
    # Check subscription access
    if not current_user.has_access_to_audiobooks():
        flash('You need a Max subscription to access audiobooks.', 'warning')
        return redirect(url_for('main.subscriptions'))
    
    audiobook = Audiobook.query.get_or_404(audiobook_id)
    
    return render_template(
        'audiobooks/player.html',
        title=f'Listening: {audiobook.title}',
        audiobook=audiobook
    )


@main_bp.route('/audiobook/<int:audiobook_id>/download')
@login_required
def download_audiobook(audiobook_id):
    """Download audiobook file."""
    # Check subscription access
    if not current_user.has_access_to_audiobooks():
        flash('You need a Max subscription to download audiobooks.', 'warning')
        return redirect(url_for('main.subscriptions'))
    
    audiobook = Audiobook.query.get_or_404(audiobook_id)
    
    # In production, this would serve the actual file
    flash(f'Downloading {audiobook.title}...', 'info')
    return redirect(url_for('main.audiobook_detail', audiobook_id=audiobook_id))