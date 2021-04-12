"""file_upload.py
    A simple file upload and file listing Flask application.

    To run this on flask webserver,
    - set up an environmental variable FLASK_APP to file_upload.py
        - in PowerShell, execute $env:FLASK_APP = "file_upload.py"
        - in CMD, set FLASK_APP=file_upload.py
    - cd into the folder where this file is
    - issue ``flask run``"""

import os
import math
import datetime
from pathlib import Path
from time import sleep
from datetime import datetime
from typing import Tuple
import pandas
import matplotlib.pyplot as plt
import numpy
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge


# user defined settings go here
from settings import *  # pylint: disable=wildcard-import

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
                          request.remote_addr, file_to_delete, "File deleted.",
                          sep="\t", file=o_file)

    folder_size = get_size(app.config['UPLOAD_PATH'])
    return render_template('list.j2',
                           files=get_files(),
                           prevent_upload=upload_disallowed(),
                           folder_size=folder_size,
                           deleted=file_to_delete,
                           limit=LIMITS)


@app.route('/download/<path:filename>')
def download(filename):
    """Sends the file to the browser as downloadable content.
        Doesn't show it, even it could be rendered."""
    filename = secure_filename(filename)
    return send_from_directory(directory=app.config['UPLOAD_PATH'],
                               filename=filename,
                               as_attachment=True)


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
                  request.remote_addr, "",
                  "File cannot be created, because the folder is full.", sep="\t", file=o_file)
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
                              new_filename,
                              "File cannot be saved: file name already exists.",
                              sep="\t", file=o_file)
                else:
                    uploaded_file.save(new_path)
                    success = True
                    with open(LOG_FNAME, "a") as o_file:
                        print(datetime.datetime.now().strftime('%Y-%m-%d-%H:%M'),
                              request.remote_addr, new_filename, "File saved.",
                              sep="\t", file=o_file)
                    sleep(0.1)
                    prevent_upload = upload_disallowed()

        except RequestEntityTooLarge as my_exception:
            print("Exception", my_exception)
            success = False
            reason = str(my_exception)

    folder_size = get_size(app.config['UPLOAD_PATH'])
    return render_template('list.j2',
                           files=get_files(),
                           prevent_upload=prevent_upload,
                           new_filename=new_filename,
                           success=success,
                           reason=reason,
                           limit=LIMITS,
                           folder_size=folder_size)


def set_def(in_val, value):
    """Sets the value if it is none."""
    if in_val is None or in_val == "":
        in_val = value
    return in_val


def create_plot(x_range: Tuple[float, float],
                func_type,
                f_params: Tuple[float, float],
                clear_plot) -> str:
    """Creates a plot and tells its static path."""

    if clear_plot is not None:
        plt.clf()

    x_range_vals = numpy.arange(x_range[0], x_range[1], 0.1)
    if func_type == "1":
        y_vals = f_params[0] * numpy.sin(x_range_vals) + f_params[1]
    elif func_type == "2":
        y_vals = f_params[0] * numpy.cos(x_range_vals) + f_params[1]
    elif func_type == "3":
        y_vals = f_params[0] * numpy.sin(x_range_vals) + \
            (1-f_params[0]) * numpy.cos(x_range_vals) + f_params[1]

    plt.plot(x_range_vals, y_vals)
    date_time = datetime.now().strftime("%m-%d-%Y--%H-%M-%S")
    ofname = "plots/" + date_time + ".png"
    plt.savefig("static/" + ofname)
    return ofname


@app.route('/plot', methods=['GET'])
def plot():
    """Plots a function using matplotlib.

    Generates the plotted function if values are provided,
    and returns a html page with the plot inserted.
    """

    func_type = request.args.get('ft')
    param_a = request.args.get('a')
    param_c = request.args.get('c')
    x_min = request.args.get('xmin')
    x_max = request.args.get('xmax')
    clear_plot = request.args.get('cp')
    ofname = ""
    if func_type is not None and param_a is not None and param_c is not None:
        func_type = str(func_type)
        f_params = (float(param_a), float(param_c))
        x_range = (float(set_def(x_min, 0)), float(set_def(x_max, 10)))
        ofname = create_plot(x_range, func_type,
                             f_params, clear_plot)
    return render_template('plot.j2', plot_fname=ofname)


def calc_plot(params, savings) -> str:
    """Create the plot file for the calc function."""
    savings = numpy.array(savings)

    years = [*range(0, params["term"][0]+1)]
    labels = years[:]
    labels[0] = "initial"
    plt.clf()

    plt.suptitle('Total savings at the end of the years')
    plt.xticks(ticks=years, labels=labels)

    plt.ylabel('Actual saving ($1000)')
    plt.xlabel('time (year)')

    plt.bar(years, savings/1000)

    date_time = datetime.now().strftime("%m-%d-%Y--%H-%M-%S")
    ofname = "calc_plots/" + date_time + ".png"
    plt.savefig("static/" + ofname, dpi=72)
    return ofname


def calc_export_excel(params, savings) -> str:
    """Writes the results into an xlsx file."""
    dataf = pandas.DataFrame(numpy.ndarray(shape=(len(savings) + 10, 2)))
    # this is just temporal, I am not serious
    dataf.iloc[1, 0] = "interest rate (%)"
    dataf.iloc[2, 0] = "yearly savings ($)"
    dataf.iloc[3, 0] = "term (year)"
    dataf.iloc[4, 0] = "initial saving ($)"
    dataf.iloc[5, 0] = "total savings ($)"

    dataf.iloc[1, 1] = params["interest_rate"][0]
    dataf.iloc[2, 1] = params["yearly_savings"][0]
    dataf.iloc[3, 1] = params["term"][0]
    dataf.iloc[4, 1] = params["initial_saving"][0]
    dataf.iloc[5, 1] = savings[-1]

    dataf.iloc[0, :] = numpy.nan
    dataf.iloc[6, :] = numpy.nan
    dataf.iloc[7, :] = numpy.nan

    dataf.iloc[8, 0] = "explanation"
    dataf.iloc[8, 1] = numpy.nan
    dataf.iloc[9, 0] = "time (year)"
    dataf.iloc[9, 1] = "balance at the end of the year ($)"

    dataf.iloc[10, 0] = "initial ($)"
    dataf.iloc[10, 1] = params["initial_saving"][0]

    for year, saving in enumerate(savings[1:]):
        dataf.iloc[11+year, 0] = year+1
        dataf.iloc[11+year, 1] = saving

    date_time = datetime.now().strftime("%m-%d-%Y--%H-%M-%S")
    ofname = "calc_plots/" + date_time + ".xlsx"
    dataf.to_excel("static/" + ofname,
                   sheet_name='savings',
                   engine="openpyxl",
                   index=False,
                   header=False)
    return ofname


@app.route('/calc', methods=['', 'GET', 'POST'])
def calc():
    """Spreadsheet example with a figure.

    Shows how some excel files can be replaced with flask."""

    success = None
    reason = ""
    new_filename = ""
    if "file" in request.files:  # if the user wants to send a file
        nowstr = datetime.now().strftime('%Y-%m-%d_%H-%M')
        if upload_disallowed():
            success = False
            reason = "The folder is full, flask didn't even try to save the file here."
            with open(LOG_FNAME) as o_file:
                print(nowstr,
                      request.remote_addr, "",
                      "File cannot be created, because the folder is full.", sep="\t", file=o_file)
        else:
            try:
                uploaded_file = request.files['file']
                new_filename = secure_filename(uploaded_file.filename)
                new_path = os.path.join(
                    app.config['UPLOAD_PATH'], nowstr + "_" + new_filename)
                if uploaded_file.filename != '':
                    if os.path.exists(new_path):
                        success = False
                        reason = "File already exists with the file name " + new_filename
                        with open(LOG_FNAME, "a") as o_file:
                            print(nowstr,
                                  request.remote_addr,
                                  new_filename,
                                  "File cannot be saved: file name already exists.",
                                  sep="\t", file=o_file)
                    else:
                        uploaded_file.save(new_path)
                        success = True
                        with open(LOG_FNAME, "a") as o_file:
                            print(nowstr,
                                  request.remote_addr, new_filename, "File saved.",
                                  sep="\t", file=o_file)
                        sleep(0.1)

            except RequestEntityTooLarge as my_exception:
                print("Exception", my_exception)
                success = False
                reason = str(my_exception)

    params = {"interest_rate": [1, "Interest rate (%)"],
              "yearly_savings": [10_000, "Yearly savings ($)"],
              "term": [10, "Term (year)"],
              "initial_saving": [100_000, "Initial saving ($)"]}

    if success:  # template file is provided and successfully saved
        dataf = pandas.read_excel(new_path, engine='openpyxl')
        params["interest_rate"][0] = dataf.iloc[0, 1]
        params["yearly_savings"][0] = dataf.iloc[1, 1]
        params["term"][0] = dataf.iloc[2, 1]
        params["initial_saving"][0] = dataf.iloc[3, 1]
    else:
        for param in params:
            read_in_val = request.args.get(param)
            if read_in_val is not None:
                params[param][0] = float(read_in_val)

    # initial saving, 0th year
    savings = [params["initial_saving"][0],
               params["initial_saving"][0] * (1 + params["interest_rate"][0]/100)]
    params["term"][0] = int(params["term"][0])

    for _ in range(0, params["term"][0]-1):
        savings.append(
            savings[-1] * (1 + params["interest_rate"][0]/100) + params["yearly_savings"][0])

    return render_template("calc.html",
                           prevent_upload=upload_disallowed(),
                           new_filename=new_filename,
                           success=success,
                           reason=reason,
                           params=params,
                           savings=savings,
                           plotfname=calc_plot(params, savings),
                           excelfname=calc_export_excel(params, savings))
