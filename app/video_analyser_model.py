# -*- encoding: utf-8 -*-
"""
Python Aplication Template
Licence: GPLv3
"""

import subprocess
import silence_removal
import os
from app import app
from datetime import datetime

class VideoAnalyser(object):
    def __init__(self, video_file):
        self.video_file = video_file
        self.file_name = ""

    def get_audio_from_video(self):
        time = datetime.now().strftime("%H:%M:%S")
        self.file_name = os.path.basename(self.video_file).split('.')[0] + time
        audio_file = self.file_name + '.wav'
        file_path_output = app.config['UPLOAD_FOLDER'] + audio_file
        subprocess.call(['ffmpeg', '-i', app.config['UPLOAD_FOLDER'] + self.video_file, '-codec:a', 'pcm_s16le', '-ac', '1',
             file_path_output])

        return file_path_output

    def get_sound_segments(self, wav):
        return silence_removal.get_voiced_segments(wav)

    def remove_silence_segments_from_video(self, segments):

        output_video = self.file_name + "_processed" + ".mp4"

        between_intervals = ""

        for index, value in enumerate(segments[:-1]):
            value_concatenated = "between(t,{0},{1})+".format(value, segments[index + 1])
            between_intervals += value_concatenated

        between_intervals = between_intervals[:-1]

        subprocess.call(['ffmpeg', '-i', app.config['UPLOAD_FOLDER'] + self.video_file, '-vf',
                         "select='{0}',setpts=N/FRAME_RATE/TB".format(between_intervals), '-af',
                         "aselect='{0}',asetpts=N/SR/TB".format(between_intervals),
             app.config['UPLOAD_FOLDER'] + output_video])

        return output_video
