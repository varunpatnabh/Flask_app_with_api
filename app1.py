# # from flask import Flask,jsonify
# from pyngrok import ngrok

# from flask import Flask, jsonify

# app = Flask(__name__)


# books = [
#     {'id': 1, 'title': 'ABC'},
#     {'id': 2, 'title': 'PQr'}
# ]

# @app.route('/api/books', methods=['GET'])
# def get_all_books():
#     return jsonify(books)

# @app.route('/api/books/<int:book_id>', methods=['GET'])
# def get_book(book_id):
#     book = next((book for book in books if book['id'] == book_id), None)
#     if book:
#         return jsonify(book)
#     else:
#         return jsonify({'error': 'Book not found'}), 404

# if __name__ == '__main__':
#     public_url = ngrok.connect(5000)
#     print(f"ngrok tunnel: {public_url}")
    
#     # Run the Flask app
#     app.run()
    
    

from pyngrok import ngrok
from flask import Flask, jsonify, redirect

app = Flask(__name__)

books = [
    {'id': 1, 'title': 'ABC'},
    {'id': 2, 'title': 'PQr'}
]

@app.route('/')
def home():
    # Redirect to /api/books
    return redirect('/api/books')

@app.route('/api/books', methods=['GET'])
def get_all_books():
    return jsonify(books)

@app.route('/api/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = next((book for book in books if book['id'] == book_id), None)
    if book:
        return jsonify(book)
    else:
        return jsonify({'error': 'Book not found'}), 404

if __name__ == '__main__':
    # Start an ngrok tunnel
    public_url = ngrok.connect(5000)
    print(f"ngrok tunnel: {public_url}")

    # Run the Flask app
    app.run(host='0.0.0.0', port=5000)

# from flask import Flask, jsonify, request, make_response

# app = Flask(__name__)

# books = [
#     {'id': 1, 'title': 'ABC'},
#     {'id': 2, 'title': 'PQr'}
# ]

# @app.after_request
# def add_ngrok_header(response):
#     response.headers['ngrok-skip-browser-warning'] = 'true'
#     return response

# @app.route('/')
# def home():
#     return jsonify({'message': 'Welcome to the book API! Visit /api/books'})

# @app.route('/api/books', methods=['GET'])
# def get_all_books():
#     return jsonify(books)

# @app.route('/api/books/<int:book_id>', methods=['GET'])
# def get_book(book_id):
#     book = next((book for book in books if book['id'] == book_id), None)
#     if book:
#         return jsonify(book)
#     else:
#         return jsonify({'error': 'Book not found'}), 404

# if __name__ == '__main__':
#     from pyngrok import ngrok
#     public_url = ngrok.connect(5000)
#     print(f"ngrok tunnel: {public_url}")
#     app.run(host='0.0.0.0', port=5000)

