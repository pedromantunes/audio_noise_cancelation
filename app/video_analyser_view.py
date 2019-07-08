# -*- encoding: utf-8 -*-
"""
Python Aplication Template
Licence: GPLv3
"""

import os
import subprocess
from flask import url_for, redirect, render_template, flash, request, g, session
from app import app
from werkzeug.utils import secure_filename
from flask import send_from_directory

UPLOAD_FOLDER = '/home/pedroantunes'
ALLOWED_EXTENSIONS = set(['mp4', '3gp'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    raw_file_name = os.path.basename(filename).split('.')[0]
    file_path_output = UPLOAD_FOLDER + '/' + raw_file_name + '.wav'
    print('processing file: %s' % '/home/pedroantunes/Downloads/' + filename)
    subprocess.call(['ffmpeg', '-i', '/home/pedroantunes/Downloads/' + filename, '-codec:a', 'pcm_s16le', '-ac', '1', file_path_output])
    print('file %s saved' % file_path_output)
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


# ====================
