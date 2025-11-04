from flask import render_template, flash, redirect, url_for, request, abort, send_file, jsonify, Response
from flask_login import login_required, current_user
from app.routes import main_bp
from app.models.ebook import Ebook, EbookFormat
from app import db
from sqlalchemy import or_
import os
import requests # type: ignore

@main_bp.route('/ebooks')
def list_ebooks():
    """Display list of ebooks with pagination. (Publicly accessible)"""
    search_term = request.args.get('q', '', type=str)
    page = request.args.get('page', 1, type=int)
    per_page = 20  # Show 20 ebooks per page
    
    if search_term:
        pagination = Ebook.query.filter(
            or_(
                Ebook.title.ilike(f'%{search_term}%'),
                Ebook.author.ilike(f'%{search_term}%')
            )
        ).order_by(Ebook.title).paginate(page=page, per_page=per_page, error_out=False)
    else:
        pagination = Ebook.query.order_by(Ebook.title).paginate(page=page, per_page=per_page, error_out=False)
    
    return render_template(
        'ebooks/list.html',
        title='Ebooks Collection',
        ebooks=pagination.items,
        pagination=pagination,
        search_term=search_term
    )


@main_bp.route('/ebook/<int:ebook_id>')
def ebook_detail(ebook_id):
    """Display ebook details. (Publicly accessible)"""
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
        return render_template('upgrade_required.html', 
                             title='Upgrade Required',
                             feature='ebooks')
    
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
        return render_template('upgrade_required.html', 
                             title='Upgrade Required',
                             feature='ebooks')
    
    ebook = Ebook.query.get_or_404(ebook_id)
    
    # In production, this would serve the actual file
    # For now, just show a message
    flash(f'Downloading {ebook.title}...', 'info')
    return redirect(url_for('main.ebook_detail', ebook_id=ebook_id))


@main_bp.route('/api/ebook/proxy')
@login_required
def ebook_proxy():
    """Proxy endpoint to fetch ebook content and avoid CORS issues."""
    url = request.args.get('url')
    
    if not url:
        return jsonify({'error': 'No URL provided'}), 400
    
    try:
        # Fetch the content from Project Gutenberg
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        # Return the content with appropriate headers
        return Response(
            response.content,
            mimetype=response.headers.get('Content-Type', 'text/plain'),
            headers={
                'Access-Control-Allow-Origin': '*',
                'Content-Type': response.headers.get('Content-Type', 'text/plain; charset=utf-8')
            }
        )
    except Exception as e:
        return jsonify({'error': f'Failed to fetch ebook: {str(e)}'}), 500