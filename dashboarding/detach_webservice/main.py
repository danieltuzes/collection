from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import csv
import datetime
import subprocess
import os
import psutil

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

UPLOAD_FOLDER = 'uploads'
LOG_PATH = 'log.csv'
STDOUT_FOLDER = 'stdout'
STDERR_FOLDER = 'stderr'

for folder in [UPLOAD_FOLDER, STDOUT_FOLDER, STDERR_FOLDER]:
    if not os.path.exists(folder):
        os.mkdir(folder)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        original_filename = uploaded_file.filename
        new_filename = f"{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.py"
        uploaded_file.save(f"{UPLOAD_FOLDER}/{new_filename}")
        stdout_path = f"{STDOUT_FOLDER}/{new_filename}.out"
        stderr_path = f"{STDERR_FOLDER}/{new_filename}.err"
        
        with open(LOG_PATH, 'a', newline='') as log_file:
            writer = csv.writer(log_file)
            writer.writerow([original_filename, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), new_filename, 'Not started', '', stdout_path, stderr_path])
        
        return redirect(url_for('index'))
    
    entries = []
    if os.path.exists(LOG_PATH):
        with open(LOG_PATH, 'r') as log_file:
            reader = csv.reader(log_file)
            for row in reader:
                if row[3] == 'Not started':
                    process = subprocess.Popen(["python", f"{UPLOAD_FOLDER}/{row[2]}"], stdout=open(row[5], 'w'), stderr=open(row[6], 'w'))
                    pid = process.pid
                    row[3] = 'Running'
                    row[4] = pid
                elif row[3] == 'Running' and not psutil.pid_exists(int(row[4])):
                    row[3] = 'Finished'
                entries.append(row)
                
        # Update log file after checking all processes
        with open(LOG_PATH, 'w', newline='') as log_file:
            writer = csv.writer(log_file)
            writer.writerows(entries)
    
    return render_template('index.html', entries=entries)

@app.route('/download/<folder>/<filename>')
def download_file(folder, filename):
    if folder in ["stdout", "stderr"]:
        return send_from_directory(folder, filename, as_attachment=True)
    else:
        return "File not found", 404

if __name__ == '__main__':
    app.run(debug=True)