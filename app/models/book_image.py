"""
Book Image Model
Stores multiple images for each physical book
"""

from app import db
from datetime import datetime


class BookImage(db.Model):
    """Model for storing book cover images"""
    __tablename__ = "book_image"
    
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('physical_book.id'), nullable=False)
    
    # Image paths (3 versions)
    original_path = db.Column(db.String(255), nullable=False)
    large_path = db.Column(db.String(255), nullable=False)
    thumbnail_path = db.Column(db.String(255), nullable=False)
    
    # Image metadata
    filename = db.Column(db.String(255), nullable=False)
    is_primary = db.Column(db.Boolean, default=False)  # Main cover image
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship
    book = db.relationship('PhysicalBook', backref=db.backref('images', lazy=True, cascade='all, delete-orphan'))
    
    def __repr__(self):
        return f"<BookImage id={self.id} book_id={self.book_id} primary={self.is_primary}>"
    
    @property
    def thumbnail_url(self):
        """Get URL for thumbnail"""
        return f"/static/{self.thumbnail_path}"
    
    @property
    def large_url(self):
        """Get URL for large image"""
        return f"/static/{self.large_path}"
    
    @property
    def original_url(self):
        """Get URL for original image"""
        return f"/static/{self.original_path}"
