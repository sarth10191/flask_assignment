from flask import Blueprint, jsonify, request
from models.BookModel import BookModel, BookSchema

book_blueprint = Blueprint("books", __name__, url_prefix="/books")
book_schema= BookSchema()


@book_blueprint.route('/', methods=['GET', 'POST'])
def get_or_create_book():
    if request.method == 'GET':
        result = BookModel.query.all()
        return jsonify(book_schema.dump(result, many=True)), 200

    elif request.method == 'POST':
        data = request.json
        errors = book_schema.validate(data)
        if errors.get("book_name"):
            return jsonify(Error="Book name cannot be empty"), 400
        elif errors.get("book_author"):
            return jsonify(Error="Author name cannot be empty"), 400
        else:
            book = BookModel(data.get("book_id"), data.get("book_name", ''), data.get("book_author", ''))
            if book.add():
                return jsonify(Message="Book added successfully"), 201
            else:
                return jsonify(Error="Book with same id already exists"), 400


@book_blueprint.route('/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = BookModel.query.get(book_id)
    if book:
        return jsonify(book_schema.dump(book)), 200
    else:
        return jsonify(Error='No book with that ID'), 400


@book_blueprint.route('/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = BookModel.query.get(book_id)
    if book:
        book.delete()
        return jsonify(Message="Success"), 204
    else:
        return jsonify(Error='No book with that ID'), 400
