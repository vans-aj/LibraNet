# app/models/audiobook.py
# (Is code se apni file ko replace karein)

from app import db
from .publication import Publication

class Audiobook(Publication):
    """
    Model for Audiobooks in the library catalog.
    Main metadata (title, author, summary) Publication se inherit hoti hai.
    """
    __tablename__ = "audiobook"

    id = db.Column(db.Integer, db.ForeignKey('publication.id'), primary_key=True)
    narrator = db.Column(db.String(150), nullable=True)
    
    # Hum yahaan LibriVox ki ID store kar sakte hain taaki future mein data refresh kar sakein
    librivox_id = db.Column(db.String(100), nullable=True, unique=True, index=True) 

    # NAYA: Ek Audiobook ke kai Chapters ho sakte hain
    # Yeh is 'Audiobook' ko 'AudiobookChapter' table se link karta hai
    chapters = db.relationship('AudiobookChapter', 
                               back_populates='audiobook', 
                               lazy='dynamic', 
                               cascade="all, delete-orphan")

    __mapper_args__ = {
        'polymorphic_identity': 'audiobook',
    }
    
    @property
    def total_duration_minutes(self):
        """Saare chapters se total duration calculate karta hai."""
        # lazy='dynamic' use kiya hai, isliye .all() zaroori hai
        all_chapters = self.chapters.all()
        if not all_chapters:
            return 0
        
        total_seconds = 0
        for c in all_chapters:
            if c.duration_seconds:
                total_seconds += c.duration_seconds
                
        return total_seconds / 60

    def __repr__(self):
        return f"<Audiobook id={self.id} title='{self.title}'>"


# NAYA MODEL: Har chapter ka MP3 link store karne ke liye
class AudiobookChapter(db.Model):
    """
    Ek audiobook ke har chapter ka MP3 link aur details store karta hai.
    Har row ek chapter hai.
    """
    __tablename__ = "audiobook_chapter"
    
    id = db.Column(db.Integer, primary_key=True)
    
    # API se mila 'live' MP3 link
    content_url = db.Column(db.String(500), nullable=False, unique=True)
    
    chapter_title = db.Column(db.String(300), nullable=True)
    chapter_number = db.Column(db.Integer, nullable=False)
    
    # Duration ko seconds mein store karna behtar hai
    duration_seconds = db.Column(db.Float, nullable=True) 
    
    # Foreign Key jo is chapter ko uski book se jodta hai
    audiobook_id = db.Column(db.Integer, db.ForeignKey('audiobook.id'), nullable=False)

    # Relationship (taaki aap chapter.audiobook se book access kar sakein)
    audiobook = db.relationship('Audiobook', back_populates='chapters')

    def __repr__(self):
        return f"<AudiobookChapter num={self.chapter_number} audiobook_id={self.audiobook_id}>"