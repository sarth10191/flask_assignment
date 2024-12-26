from flask import request, jsonify, Blueprint
from ..models.BorrowModel import BorrowModel, BorrowSchema
from ..models.BookModel import BookModel, BookSchema
from ..models.UserModel import UserModel
from datetime import datetime

borrow_blueprint = Blueprint('borrows', __name__, url_prefix='/borrows')
borrow_schema = BorrowSchema()
book_schema = BookSchema()


@borrow_blueprint.route('/', methods=['GET'])
def get_borrowed_list():
    result = BorrowModel.query.all()
    return jsonify(borrow_schema.dump(result, many=True)), 200


@borrow_blueprint.route('/', methods=['POST'])
def create_borrow_request():
    data = request.json
    book = BookModel.query.get(data.get("book_id"))
    if not UserModel.query.get(data.get("user_id")):
        return jsonify(Error="No user with that ID"), 400
    elif not book:
        return jsonify(Error="No book with that ID"), 400
    elif not book.book_available:
        return jsonify(Error="Book not available"), 400
    else:
        book.book_available = False
        borrow = BorrowModel(data.get("book_id"), data.get("user_id"),
                             datetime.strptime(data.get("borrowing_date"), "%Y-%m-%d"),
                             datetime.strptime(data.get("till_date"), "%Y-%m-%d"))

        borrow.add()
        return jsonify(Message='Successfully borrowed'), 200


@borrow_blueprint.route('/<int:borrow_id>', methods=['GET'])
def get_borrow_request(borrow_id):
    result = BorrowModel.query.get(borrow_id)
    if result:
        return jsonify(borrow_schema.dump(result)), 200
    else:
        return jsonify(Error='No details found with that ID'), 400


@borrow_blueprint.route('/availablebooks', methods=['GET'])
def get_available_books():
    result = BookModel.query.filter(BookModel.book_available == True)
    return jsonify(book_schema.dump(result, many=True)), 200
