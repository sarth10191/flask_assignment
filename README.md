Library Management System
This project is a simple Library Management System built using Flask, SQLAlchemy, and Marshmallow. It allows users to manage books, users, and borrowing transactions.
Features
User Management: Create, retrieve, and delete users.
Book Management: Add, retrieve, and delete books.
Borrowing System: Users can borrow books and generate bills upon returning them.
API Endpoints
User Endpoints
GET /users/: Retrieve all users.
POST /users/: Create a new user.
GET /users/<user_id>: Retrieve a user by ID.
DELETE /users/<user_id>: Delete a user by ID.
Book Endpoints
GET /books/: Retrieve all books.
POST /books/: Add a new book.
GET /books/<book_id>: Retrieve a book by ID.
DELETE /books/<book_id>: Delete a book by ID.
Borrowing Endpoints
GET /borrows/: Retrieve all borrowing records.
POST /borrows/: Create a new borrowing record.
GET /borrows/<borrow_id>: Retrieve a borrowing record by ID.
GET /borrows/availablebooks: Get a list of available books.
Billing Endpoints
POST /bills/: Generate a bill for returned books.
GET /bills/<bill_id>: Retrieve a bill by ID.
Running the Application
To run the application, execute the appropriate command in your environment. The application will be available at http://127.0.0.1:8000.