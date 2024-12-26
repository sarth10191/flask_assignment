from flask import request, jsonify, Blueprint
from models.BillingModel import BillingModel, BillingSchema
from models.BorrowModel import BorrowModel
from models.BookModel import BookModel
from datetime import datetime

bill_blueprint = Blueprint('bills', __name__, url_prefix='/bills')
bill_schema = BillingSchema()


def get_bill_amount(issue_date, till_date, return_date, charge=10, fine=20):
    amount = (till_date - issue_date).days * charge
    if return_date > till_date:
        amount += (return_date - till_date).days * fine
    return amount


@bill_blueprint.route('/', methods=['POST'])
def create_bill():
    data = request.json
    borrow_id = data.get("borrow_id")
    return_date = datetime.strptime(data.get("return_date"), "%Y-%m-%d")

    if return_date < datetime.today():
        return jsonify(Error='Return date cannot be in past'), 400

    borrow = BorrowModel.query.get(borrow_id)
    if borrow.is_returned:
        return jsonify(Error='Book already returned'), 400
    else:
        bill_amount = get_bill_amount(issue_date=borrow.borrowing_date,
                                      till_date=borrow.till_date,
                                      return_date=return_date,
                                      charge=10, fine=20)
        borrow.is_returned = True
        BookModel.query.get(borrow.book_id).book_available = True
        BillingModel(borrow_id, return_date, bill_amount).add()
        return jsonify(Message='Bill generated'), 200


@bill_blueprint.route('/<int:bill_id>', methods=['GET'])
def get_bill(bill_id):
    bill = BillingModel.query.get(bill_id)
    if bill:
        return jsonify(bill_schema.dump(bill)), 200
    else:
        return jsonify(Error='No bill with that ID'), 400
