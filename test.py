import requests

BASE_URL = "http://127.0.0.1:8000"

def test_users():
    response = requests.post(f"{BASE_URL}/users/", json={"user_id": 1, "user_name": "Sarth"})
    print("Create User:", response.text)
    response = requests.get(f"{BASE_URL}/users/")
    print("Get Users:", response.text)
    response = requests.get(f"{BASE_URL}/users/1")
    print("Get User:", response.text)
    response = requests.delete(f"{BASE_URL}/users/1")
    print("Delete User:", response.status_code)

def test_books():
    response = requests.post(f"{BASE_URL}/books/", json={"book_id": 1, "book_name": "Python Programming", "book_author": "Jane Smith"})
    print("Create Book:", response.text)
    response = requests.get(f"{BASE_URL}/books/")
    print("Get Books:", response.text)

    response = requests.get(f"{BASE_URL}/books/1")
    print("Get Book:", response.text)
    response = requests.delete(f"{BASE_URL}/books/1")
    print("Delete Book:", response.status_code)

if __name__ == "__main__":
    test_users()
    test_books()

# Create User: {
#   "Message": "User registered successfully"
# }

# Get Users: [
#   {
#     "user_id": 1,
#     "user_name": "Sarth"
#   }
# ]

# Get User: {
#   "user_id": 1,
#   "user_name": "Sarth"
# }

# Delete User: 204
# Create Book: {
#   "Message": "Book added successfully"
# }

# Get Books: {
#   "books": [
#     {
#       "book_author": "Jane Smith",
#       "book_available": true,
#       "book_id": 1,
#       "book_name": "Python Programming"
#     }
#   ],
#   "current_page": 1,
#   "pages": 1,
#   "total": 1
# }

# Get Book: {
#   "book_author": "Jane Smith",
#   "book_available": true,
#   "book_id": 1,
#   "book_name": "Python Programming"
# }

# Delete Book: 204
