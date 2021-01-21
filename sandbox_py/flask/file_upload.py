"""file_upload.py
    A simple file upload and file listing Flask application."""

import os
from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
from time import sleep


def get_size(folder_to_check):
    """Returns the size of the folder."""
    root_directory = Path(folder_to_check)
    return sum(f.stat().st_size for f in root_directory.glob('**/*') if f.is_file())


app = Flask(__name__)
app.config['UPLOAD_PATH'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024
FOLDER_SIZE_LIMIT = 850 * 1024  # 850 KB


@app.route('/')
def index():
    """Returns the ``index.html`` file."""
    files = os.listdir(app.config['UPLOAD_PATH'])
    return render_template('index.html', files=files)


@app.route('/', methods=['POST'])
def upload_file():
    """What to do with the uploaded file."""
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    if uploaded_file.filename != '':
        uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
    return redirect(url_for('index'))


@app.route('/listfile')
def listfiles():
    """Returns the ``list.html`` file."""
    files = os.listdir(app.config['UPLOAD_PATH'])
    prevent_upload = False

    used_storage = get_size(app.config['UPLOAD_PATH'])
    if used_storage > FOLDER_SIZE_LIMIT:
        prevent_upload = True

    return render_template('list.html', files=files, prevent_upload=prevent_upload)


@app.route('/submit', methods=['POST'])
def submit():
    """Saves the updloaded file and sends confirmation."""
    files = os.listdir(app.config['UPLOAD_PATH'])
    prevent_upload = False
    success = False
    reason = ""
    filename = ""

    used_storage = get_size(app.config['UPLOAD_PATH'])
    if used_storage > FOLDER_SIZE_LIMIT:
        success = False
        prevent_upload = True
        reason = "The folder is full, flask didn't even try to save the file here."
    else:
        try:
            uploaded_file = request.files['file']
            filename = secure_filename(uploaded_file.filename)
            if uploaded_file.filename != '':
                uploaded_file.save(os.path.join(
                    app.config['UPLOAD_PATH'], filename))
                success = True
                sleep(0.1)
                files = os.listdir(app.config['UPLOAD_PATH'])
        except RequestEntityTooLarge:
            success = False
            reason = "File was too large."

    used_storage = get_size(app.config['UPLOAD_PATH'])
    if used_storage > FOLDER_SIZE_LIMIT:
        prevent_upload = True

    return render_template('list.html', files=files, prevent_upload=prevent_upload,
                           success=success, new_filename=filename, reason=reason)
