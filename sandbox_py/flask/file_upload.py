"""file_upload.py
    A simple file upload and file listing Flask application.

    To run this on flask webserver,
    - set up an environmental variable FLASK_APP to file_upload.py
    - cd into the folder where this file is
    - issue ``flask run``"""

import os
import math
import datetime
from pathlib import Path
from time import sleep
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
from settings import *  # user defined settings go here

LIMITS = {"file_size": MAX_CONTENT_LENGTH,
          "folder_size": FOLDER_SIZE_LIMIT, "file_count": FILE_COUNT_LIMIT}


def get_size(folder_to_check):
    """Returns the size of the folder."""
    root_directory = Path(folder_to_check)
    return sum(f.stat().st_size for f in root_directory.glob('**/*') if f.is_file())


def get_list_of_files():
    """Counts the files in the upload directory except the files that should be ignored."""
    files = os.listdir(app.config['UPLOAD_PATH'])
    files.sort()

    for ignore_file in IGNORE_FILES:
        if ignore_file in files:
            files.remove(ignore_file)

    return files


def get_files():
    """Gets the list of files with some properties."""
    filenames = get_list_of_files()
    file_sizes = []
    file_ctimes = []    # creation date
    for file in filenames:
        properties = os.stat(app.config['UPLOAD_PATH'] + "/" + file)
        file_sizes.append(math.ceil(properties.st_size/1024))
        file_ctimes.append(datetime.datetime.fromtimestamp(
            properties.st_ctime).strftime('%Y-%m-%d-%H:%M'))

    files = list(zip(filenames, file_sizes, file_ctimes))

    return files


def too_much_storage_is_used():
    """Tells if the upload directory uses too much disk space."""
    used_storage = get_size(app.config['UPLOAD_PATH'])
    if used_storage > FOLDER_SIZE_LIMIT:
        return True

    return False


def too_many_files():
    """Tells if too many files are in the upload directory."""
    file_list = get_list_of_files()
    if len(file_list) >= FILE_COUNT_LIMIT:
        return True

    return False


def upload_disallowed():
    """Returns false is for some security or performance reason the upload should be blocked."""
    return too_much_storage_is_used() or too_many_files()


app = Flask(__name__)
app.config['UPLOAD_PATH'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH


@app.route('/')
def index():
    """Returns the ``index.j2`` file."""
    files = os.listdir(app.config['UPLOAD_PATH'])
    return render_template('index.j2', files=files)


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
    """Returns the ``list.j2`` file."""
    folder_size = get_size(app.config['UPLOAD_PATH'])
    return render_template('list.j2', files=get_files(), prevent_upload=upload_disallowed(), folder_size=folder_size, limit=LIMITS)


@app.route('/delfile', methods=['GET'])
def delfile():
    """Returns confirm deletion."""
    file_to_delete = request.args.get('del')
    file_infos = get_files()
    file_names = [file[0] for file in file_infos]
    if file_to_delete is not None and file_to_delete in file_names:
        if request.args.get('confirmed') is None:
            return render_template('del_confirmation.j2', file=file_to_delete)
        else:
            if file_to_delete in file_names:
                os.remove(app.config['UPLOAD_PATH'] + "/" + file_to_delete)
                with open(LOG_FNAME, "a") as o_file:
                    print(datetime.datetime.now().strftime('%Y-%m-%d-%H:%M'),
                          request.remote_addr, file_to_delete, "File deleted.", sep="\t", file=o_file)

    folder_size = get_size(app.config['UPLOAD_PATH'])
    return render_template('list.j2', files=get_files(), prevent_upload=upload_disallowed(), folder_size=folder_size, deleted=file_to_delete, limit=LIMITS)


@app.route('/download/<path:filename>')
def download(filename):
    filename = secure_filename(filename)
    return send_from_directory(directory=app.config['UPLOAD_PATH'], filename=filename, as_attachment=True)


@app.route('/submit')
def submit_empty():
    """If somebody passes the submit as a link, don't die"""
    return redirect(url_for('listfiles'))


@app.route('/submit', methods=['GET', 'POST'])
def submit():
    """Saves the uploaded file and sends confirmation."""
    prevent_upload = False
    success = False
    reason = ""
    new_filename = ""

    if upload_disallowed():
        success = False
        prevent_upload = True
        reason = "The folder is full, flask didn't even try to save the file here."
        with open(LOG_FNAME) as o_file:
            print(datetime.datetime().now().strftime('%Y-%m-%d-%H:%M'),
                  request.remote_addr, "", "File cannot be created, because the folder is full.", sep="\t", file=o_file)
    else:
        try:
            uploaded_file = request.files['file']
            new_filename = secure_filename(uploaded_file.filename)
            new_path = os.path.join(app.config['UPLOAD_PATH'], new_filename)
            if uploaded_file.filename != '':
                if os.path.exists(new_path):
                    success = False
                    reason = "File already exists with the file name " + new_filename
                    with open(LOG_FNAME, "a") as o_file:
                        print(datetime.datetime.now().strftime('%Y-%m-%d-%H:%M'),
                              request.remote_addr,
                              new_filename, "File cannot be saved: file name already exists.", sep="\t", file=o_file)
                else:
                    uploaded_file.save(new_path)
                    success = True
                    with open(LOG_FNAME, "a") as o_file:
                        print(datetime.datetime.now().strftime('%Y-%m-%d-%H:%M'),
                              request.remote_addr, new_filename, "File saved.", sep="\t", file=o_file)
                    sleep(0.1)
                    prevent_upload = upload_disallowed()

        except RequestEntityTooLarge as my_exception:
            print("Exception", my_exception)
            success = False
            reason = str(my_exception)

    folder_size = get_size(app.config['UPLOAD_PATH'])
    return render_template('list.j2', files=get_files(), prevent_upload=prevent_upload,
                           new_filename=new_filename, success=success, reason=reason, limit=LIMITS, folder_size=folder_size)
