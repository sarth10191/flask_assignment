from api import db
from marshmallow import Schema, fields, validate
from datetime import datetime
class BorrowModel(db.Model):
    __tablename__="borrows"
    id = db.Column(db.Integer, primary_key = True, autoincrement= True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.book_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.book_id'))
    boerrowing_date = db.Column(db.DateTime, default = datetime.now())
    till_date = db.Column(db.DateTime)
    is_returned = db.Column(db.Boolean)

    def __init__(self, book_id, user_id, borrowing_date, till_date, is_returned=False):
        self.book_id = book_id
        self.user_id = user_id
        self.boerrowing_date = borrowing_date
        self.till_date = till_date
        self.is_returned=is_returned
            
    def add(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete()
        db.session.commit()

class BorrowSchema(Schema):
    book_id = fields.Integer(required=True)
    user_id = fields.Integer(required=True)
    borrowing_date = fields.Date(required=True)
    till_date = fields.Date(required=True)
    is_returned = fields.Boolean(required=False)

