from api import db
from marshmallow import Schema, fields, validate

class BookModel(db.Model):
    __tablename__ = "books"
    book_id = db.Column(db.Integer, primary_key = True)
    book_name = db.Column(db.String(100), nullable = False)
    book_author = db.Column(db.String(100), nullable = False)
    book_available = db.Column(db.Bollean)
    borrewed = db.relationship("BorrowedModel", backref="books", lazy = "dynamic")

    def __init__(self, _id, name, author_name, available=True):
        self.book_id = _id
        self.book_name = name
        self.book_author = author_name
        self.book_available= available
    
    def add(self):
        if not self.check():
            db.session.add(self)
            db.session.commit()
            return True
        return False
    
    def check(self):
        return db.session.query(self.__class__).get(self.book_id)
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    

class BookSchema(Schema):
    book_id = fields.Int(required = True)
    book_name = fields.Str(required=True, validate=validate.Length(max=100))
    book_author = fields.Str(required=True, validate=validate.Length(max=100))
    book_available = fields.Bool(required = False)