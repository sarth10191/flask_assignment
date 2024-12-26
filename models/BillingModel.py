from api import db
from marshmallow import fields, Schema

class BillingModel(db.Model):
    __tablename__ = 'bills'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    borrow_id = db.Column(db.Integer, db.ForeignKey('borrows.id'))
    return_date = db.Column(db.DateTime)
    bill_amount = db.Column(db.Float)

    def __init__(self, borrow_id, return_date, bill_amount):
        self.borrow_id = borrow_id
        self.return_date = return_date
        self.bill_amount = bill_amount

    def add(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class BillingSchema(Schema):
    borrow_id = fields.Integer(required=True)
    return_date = fields.Date(required=True)
    bill_amount = fields.String(required=True)
