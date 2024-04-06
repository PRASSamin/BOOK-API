from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Library(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(50), unique=True)
    bookName = db.Column(db.String(80), nullable=False)
    bookThumbnail = db.Column(db.String(200), nullable=True)
    bookAuthor = db.Column(db.String(80), nullable=False)
    sLink = db.Column(db.String(200), nullable=False)
    bookWebsite = db.Column(db.String(200), nullable=True)
    bookPublisher = db.Column(db.String(80), nullable=False)
    bookPublished = db.Column(db.String(80), nullable=True)
    bookGenre = db.Column(db.String(80), nullable=False)
    country = db.Column(db.String(80), nullable=True)
    bookLang = db.Column(db.String(80), nullable=True)
    bookDesc = db.Column(db.String(500), nullable=True)

    def to_dict(self):
        return {
            'Unique ID': self.uid,
            'id': self.id,
            'name': self.bookName,
            'thumbnail': self.bookThumbnail,
            'author': self.bookAuthor,
            'source': self.sLink,
            'website': self.bookWebsite,
            'publisher': self.bookPublisher,
            'published': self.bookPublished,
            'genre': self.bookGenre,
            'country': self.country,
            'language': self.bookLang,
            'description': self.bookDesc
        }
