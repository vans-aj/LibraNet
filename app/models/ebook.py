# app/models/ebook.py
# (Yeh naya, corrected code hai)

from app import db
from .publication import Publication

class Ebook(Publication):
    """
    Model for Ebooks in the library catalog.
    Main metadata Publication se inherit hoti hai.
    """
    __tablename__ = "ebook"

    id = db.Column(db.Integer, db.ForeignKey('publication.id'), primary_key=True)
    
    external_id = db.Column(db.String(100), nullable=True, unique=True, index=True)

    # ---- YAHAA BADLAAV HAI (Line 1) ----
    # Humne 'back_ref' ko 'back_populates' se badal diya hai
    formats = db.relationship('EbookFormat', 
                              back_populates='ebook',  # <-- Yahaan badlaav hai
                              lazy=True, 
                              cascade="all, delete-orphan")

    __mapper_args__ = {
        'polymorphic_identity': 'ebook',
    }
    
    def __repr__(self):
        return f"<Ebook id={self.id} title='{self.title}'>"


# NAYA MODEL: Har format ka URL store karne ke liye
class EbookFormat(db.Model):
    """
    Ek ebook ke alag-alag file formats (EPUB, HTML, TXT) ka link store karta hai.
    Har row ek format hai.
    """
    __tablename__ = "ebook_format"
    
    id = db.Column(db.Integer, primary_key=True)
    
    # e.g., 'EPUB', 'HTML', 'TXT', 'PDF'
    file_format = db.Column(db.String(20), nullable=False)
    
    # API se mila 'live' URL
    content_url = db.Column(db.String(500), nullable=False, unique=True)
    
    # Foreign Key jo is format ko uski book se jodta hai
    ebook_id = db.Column(db.Integer, db.ForeignKey('ebook.id'), nullable=False)

    # ---- YAHAA BADLAAV HAI (Line 2) ----
    # Yeh relationship ka doosra hissa hai (jo pehle missing tha)
    ebook = db.relationship('Ebook', back_populates='formats')

    def __repr__(self):
        return f"<EbookFormat format={self.file_format} ebook_id={self.ebook_id}>"