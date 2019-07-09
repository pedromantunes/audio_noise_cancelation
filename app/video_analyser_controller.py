# -*- encoding: utf-8 -*-
"""
Python Aplication Template
Licence: GPLv3
"""

import os
from flask import url_for, redirect, flash, request, jsonify
from app import app
from werkzeug.utils import secure_filename
from flask import send_from_directory
from flask_json import FlaskJSON, JsonError, json_response, as_json
import uuid

from video_analyser_model import VideoAnalyser
from flask import render_template

from uuid import uuid4

ALLOWED_EXTENSIONS = set(['mp4'])

connection_status = {}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/get_status', methods=['GET'])
def get_status():
    id = request.args.get('id')
    return jsonify(connection_status.get(id[1:-1]))

@app.route('/', methods=['GET'])
def get_view():
    return render_template('index.html')

@app.route('/get_id', methods=['GET'])
def get_id():
    token = str(uuid.uuid4())
    connection_status[token] = 'initial'
    return jsonify(token)

@app.route('/', methods=['POST'])
def upload_file():
    token = request.form['token']
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

        # create video analyser instance with the video uploaded
        video_analyser = VideoAnalyser(filename)

        token = token.rstrip()
        token_key = token[1:-1]

        connection_status[token_key] = 'initial'

        # get wav file from video
        wav = video_analyser.get_audio_from_video()

        connection_status[token_key] = 'audio_extracted'

        # get silence segments from wav file
        silence_segments = video_analyser.get_sound_segments(wav)

        connection_status[token_key] = 'silence_segments'

        # remove silence segments from video
        ouput_video = video_analyser.remove_silence_segments_from_video(silence_segments)

        connection_status[token_key] = 'silence_removed'

        return redirect(url_for('uploaded_file',
                                filename=ouput_video))

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)