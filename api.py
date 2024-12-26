from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]= 'sqlite:///librarymanagement.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False

db=SQLAlchemy(app)
db.init_app(app)

@app.before_first_request
def create_db():
    db.create_all()

migrate = Migrate(app=app, db=db)
from views.UserView import user_blueprint
from views.BookView import book_blueprint
from views.BorrowView import borrow_blueprint

app.register_blueprint(user_blueprint)
app.register_blueprint(book_blueprint)
app.register_blueprint(borrow_blueprint)

if __name__=="__main__":
    app.run(debug=True, port = 8000)