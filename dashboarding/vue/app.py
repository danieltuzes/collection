import os
from flask import Flask, request, redirect, url_for, send_from_directory, render_template, jsonify
from werkzeug.utils import secure_filename
import pandas as pd

ALLOWED_EXTENSIONS = {'csv', 'zip'}

app = Flask(__name__, template_folder='frontend/templates', static_folder='frontend/static')
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'output'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

if not os.path.exists(app.config['OUTPUT_FOLDER']):
    os.makedirs(app.config['OUTPUT_FOLDER'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/process-csv', methods=['POST'])
def process_csv():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # Read CSV file and process it
            df = pd.read_csv(file_path)
            df['result'] = df['value'] * df['share']

            # Save the output file
            output_filename = f"{os.path.splitext(filename)[0]}_output.csv"
            output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)
            df.to_csv(output_path, index=False)

            # Return the output filename as a JSON object
            return jsonify({'output_filename': output_filename})

        return "Invalid file type", 400
    return "Invalid request", 400

@app.route('/download/<filename>')
def download_output(filename):
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename)

if __name__ == '__main__':
    app.run(debug=True)