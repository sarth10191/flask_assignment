from flask import Flask, Blueprint, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from marshmallow import fields, Schema, validate
from datetime import datetime


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]= 'sqlite:///librarymanagement.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False

db=SQLAlchemy()
db.init_app(app)


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

class BookModel(db.Model):
    __tablename__ = "books"
    book_id = db.Column(db.Integer, primary_key = True)
    book_name = db.Column(db.String(100), nullable = False)
    book_author = db.Column(db.String(100), nullable = False)
    book_available = db.Column(db.Boolean)
    borrewed = db.relationship("BorrowModel", backref="books", lazy = "dynamic")

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

class UserModel(db.Model):
    __tablename__="users"
    user_id = db.Column(db.Integer, primary_key = True)
    user_name = db.Column(db.String(255), nullable = False)
    borrows = db.relationship('BorrowModel', backref='users', lazy='dynamic')

    def __init__(self, _id, name):
        self.user_id = _id
        self.user_name = name
    
    def add(self):
        if not self.check():
            db.session.add(self)
            db.session.commit()
            return True
        return False
    
    def check(self):
        return db.session.query(self.__class__).get(self.user_id)
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

class UserSchema(Schema):
    user_id = fields.Int(required=True)
    user_name = fields.Str(required=True, validate=validate.Length(min=1))

class BorrowModel(db.Model):
    __tablename__="borrows"
    id = db.Column(db.Integer, primary_key = True, autoincrement= True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.book_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
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

user_blueprint = Blueprint("users", __name__, url_prefix="/users")
user_schema = UserSchema()

@user_blueprint.route('/', methods=['GET', 'POST'])
def users():
    if request.method == 'GET':
        result = UserModel.query.all()
        return jsonify(user_schema.dump(result, many=True)), 200

    elif request.method == 'POST':
        data = request.json
        errors = user_schema.validate(data)
        if errors:
            return jsonify(Error="User name cannot be empty"), 400
        else:
            user = UserModel(data.get("user_id"), data.get("user_name"))
            if user.add():
                return jsonify(Message="User registered successfully"), 201
            else:
                return jsonify(Error="User with same id already exists"), 400

@user_blueprint.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = UserModel.query.get(user_id)
    if user:
        return jsonify(user_schema.dump(user)), 200
    else:
        return jsonify(Message='No user with that ID'), 400

@user_blueprint.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = UserModel.query.get(user_id)
    if user:
        user.delete()
        return jsonify(Message="Success"), 204
    else:
        return jsonify(Error='No user with that ID'), 400

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
    try:
        user = UserModel.query.get(1)
    except Exception as e:
        print(e)
    print(user, data.get("user_id"))
    if not user:
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

book_blueprint = Blueprint("books", __name__, url_prefix="/books")
book_schema= BookSchema()

@book_blueprint.route('/', methods=['GET', 'POST'])
def get_or_create_book():
    if request.method == 'GET':
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 2, type=int)
        result = BookModel.query.paginate(page=page, per_page=per_page, error_out=False)
        return jsonify({
            "books": book_schema.dump(result.items, many=True),
            "total": result.total,
            "pages": result.pages,
            "current_page": result.page
        }), 200
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

@app.before_request
def create_db():
    db.create_all()
migrate = Migrate(app=app, db=db)

app.register_blueprint(user_blueprint)
app.register_blueprint(book_blueprint)
app.register_blueprint(borrow_blueprint)
app.register_blueprint(bill_blueprint)

if __name__=="__main__":
    app.run(debug=True, port = 8000)

