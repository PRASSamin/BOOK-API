from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Library(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.String(50), unique=True)
    bookName = db.Column(db.String(80), nullable=False)
    bookThumbnail = db.Column(db.String(200), nullable=True)
    bookAuthor = db.Column(db.String(80), nullable=False)
    bookWebsite = db.Column(db.String(200), nullable=True)
    bookPublisher = db.Column(db.String(80), nullable=False)
    bookPublished = db.Column(db.String(80), nullable=False)
    bookGenre = db.Column(db.String(80), nullable=False)
    country = db.Column(db.String(80), nullable=False)
    bookLang = db.Column(db.String(80), nullable=False)
    bookDesc = db.Column(db.Text, nullable=True)
    noOfPage = db.Column(db.Integer, nullable=False)
    eBook = db.Column(db.String(100), nullable=False)
    isbn = db.Column(db.String(100), nullable=False)
    bookChar = db.Column(db.Text, nullable=False)

    def to_dict(self):
        
        formatAuthorN = self.bookAuthor.split("$")
        formatPublisherN = self.bookPublisher.split("$")
        formatPublishedD = self.bookPublished.split("$")
        formatBookL = self.bookLang.split("$")
        formatBookGenre = self.bookGenre.split("$")
        formatCountry = self.country.split("$")
        if self.isbn.__contains__("-"):
            filterISBN = self.isbn.replace("-", "")
        else:
            filterISBN = self.isbn
        formatISBN = filterISBN.split("$")
        formatChar = self.bookChar.split("$")
        page = int(self.noOfPage)

        return {
            'Unique ID': self.uid,
            'id': self.id,
            'name': self.bookName,
            'ISBN': [ISBN for ISBN in formatISBN],
            'author': [authors for authors in formatAuthorN],
            'publisher': [publisher for publisher in formatPublisherN],
            'published': [published for published in formatPublishedD],
            'genre': [genre for genre in formatBookGenre],
            'country': [countr for countr in formatCountry],
            'language': [language for language in formatBookL],
            'no of pages': page,
            'ebook': self.eBook,
            'characters': [character for character in formatChar],
            'thumbnail': self.bookThumbnail,
            'website': self.bookWebsite,
            'description': self.bookDesc,
        } 