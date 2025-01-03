from flask import Flask, jsonify, request, redirect, render_template
from pyngrok import ngrok
from werkzeug.utils import secure_filename
import os
import PyPDF2
from datetime import datetime

# Flask app setup
app = Flask(__name__)

# Configure upload folder and allowed extensions
UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'pdf'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create upload folder if not exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Shared variable to store word count data
word_count_data = []

# Helper function to check file extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Function to count words in a PDF
def count_words_in_pdf(filepath):
    with open(filepath, 'rb') as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
        words = text.split()
        return len(words)

# Endpoint to upload PDFs and get word count
@app.route('/api/upload', methods=['POST'])
def upload_files():
    global word_count_data  # Use the global variable
    word_count_data = []  # Clear previous data

    # Check if the request has files
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request. Make sure the key is named "file".'}), 400

    files = request.files.getlist('file')
    if not files:
        return jsonify({'error': 'No files selected for uploading'}), 400

    for file in files:
        # Check if the file is allowed
        if file and allowed_file(file.filename):
            # Secure the filename and add a timestamp
            original_filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{os.path.splitext(original_filename)[0]}_{timestamp}{os.path.splitext(original_filename)[1]}"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            
            file.save(filepath)

            # Parse PDF to count words
            try:
                word_count = count_words_in_pdf(filepath)
                word_count_data.append({'filename': filename, 'word_count': word_count})
                # os.remove(filepath)  # Clean up after processing
            except Exception as e:
                word_count_data.append({'filename': filename, 'error': f'Error processing PDF: {str(e)}'})

        else:
            word_count_data.append({'error': f'Invalid file type for {file.filename}. Only PDF files are allowed.'})
    
    return jsonify(word_count_data), 200

# Endpoint to render the word count data on a webpage
@app.route('/homepage', methods=['GET'])
def show_count():
    global word_count_data
    return render_template('homepage.html', word_count_data=word_count_data)

# HTML for the home page
@app.route('/')
def home():
    return redirect('/homepage')

# Integrate ngrok for public URL
if __name__ == '__main__':
    public_url = ngrok.connect(5000)
    print(f"ngrok tunnel: {public_url}")
    app.run(host='0.0.0.0', port=5000)
