# from flask import Flask,jsonify,request
# from pyngrok import ngrok
# from werkzeug.utils import secure_filename
# import os
# import PyPDF2

# app = Flask(__name__)

# UPLOAD_FOLDER = './uploads'
# alwd_extns = {'pdf'}
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# os.makedirs(UPLOAD_FOLDER,exist_ok= True)

# def allowed_file(filename):
#     return '.' in filename and filename.rsplit('.',1)[1].lower() in alwd_extns

# @app.route('/api/upload',methods=['POST'])
# def upload_file():
#     if 'file' not in request.files:
#         return jsonify({'error': 'No file part in the request'}), 400
    
#     file = request.files['file']
    
#     if file.filename == '':
#         return jsonify({'error': 'No file selected'}), 400

#     if file and allowed_file(file.filename):
#         filename = secure_filename(file.filename)
#         filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
#         file.save(filepath)

#         # Parse PDF to count words
#         try:
#             word_count = count_words_in_pdf(filepath)
#             os.remove(filepath)  # Clean up after processing
#             return jsonify({'filename': filename, 'word_count': word_count}), 200
#         except Exception as e:
#             return jsonify({'error': f'Error processing PDF: {str(e)}'}), 500

#     return jsonify({'error': 'Invalid file type. Only PDF files are allowed.'}), 400

# # Function to count words in a PDF
# def count_words_in_pdf(filepath):
#     with open(filepath, 'rb') as pdf_file:
#         reader = PyPDF2.PdfReader(pdf_file)
#         text = ''
#         for page in reader.pages:
#             text += page.extract_text()
#         words = text.split()
#         return len(words)

# # Integrate ngrok for public URL
# if __name__ == '__main__':
#     public_url = ngrok.connect(5000)
#     print(f"ngrok tunnel: {public_url}")
#     app.run(host='0.0.0.0', port=5000)
    

from flask import Flask, jsonify, request
from pyngrok import ngrok
from werkzeug.utils import secure_filename
import os
import PyPDF2

# Flask app setup
app = Flask(__name__)

# Configure upload folder and allowed extensions
UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create upload folder if not exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Helper function to check file extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Endpoint to upload PDF and get word count
@app.route('/api/upload', methods=['POST'])
def upload_file():
    # Check if the request has the file part
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request. Make sure the key is named "file".'}), 400
    
    file = request.files['file']
    
    # Check if a file is selected
    if file.filename == '':
        return jsonify({'error': 'No file selected for uploading'}), 400

    # Check if the file is allowed
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Parse PDF to count words
        try:
            word_count = count_words_in_pdf(filepath)
            os.remove(filepath)  # Clean up after processing
            return jsonify({'filename': filename, 'word_count': word_count}), 200
        except Exception as e:
            return jsonify({'error': f'Error processing PDF: {str(e)}'}), 500

    return jsonify({'error': 'Invalid file type. Only PDF files are allowed.'}), 400

# Function to count words in a PDF
def count_words_in_pdf(filepath):
    with open(filepath, 'rb') as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
        words = text.split()
        return len(words)

# Integrate ngrok for public URL
if __name__ == '__main__':
    public_url = ngrok.connect(5000)
    print(f"ngrok tunnel: {public_url}")
    app.run(host='0.0.0.0', port=5000)
