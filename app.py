import os
import pandas as pd
from flask import Flask, request, render_template

app = Flask(__name__)

# Configuration for file uploads
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Max file size: 16MB

# Ensure the upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')
def upload_form():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part in the request"
    file = request.files['file']
    if file.filename == '':
        return "No file selected"
    
    if file:
        # Save the uploaded file
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        
        # Load and explore the data with Pandas
        df = pd.read_csv(file_path)
        
        # Get basic information
        data_info = df.info()
        data_preview = df.head().to_html()  # Display the first few rows in HTML format
        
        return f"""
        <h1>File uploaded successfully: {file.filename}</h1>
        <h2>Basic Data Info:</h2>
        <pre>{data_info}</pre>
        <h2>First 5 Rows:</h2>
        {data_preview}
        """
    
if __name__ == "__main__":
    app.run(debug=True)
