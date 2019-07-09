#! /usr/bin/env python
# encoding: utf-8


import numpy
import scipy.io.wavfile as wf

time_interval = 0.5 # seconds

class SoundAnalyser:

    def __init__(self):
        self.buffer_size = 160
        self.buffer = numpy.array([], dtype=numpy.int16)
        self.threshold = 0.
        self.sound_n = 0.
        self.silence_counter = 0
        self.second_spent = 0
        self.silence_segments = 0
        self.silence_elements_per_second = list()
        self.frame_elements = 300 * time_interval
        self.time_counter = 0

    # silence activity detection
    def silence_activity_detection(self, _frame):
        frame = numpy.array(_frame) ** 2.
        result = True
        fixed_threshold = 0.1
        thd = numpy.min(frame) + numpy.ptp(frame) * fixed_threshold
        self.threshold = (self.sound_n * self.threshold + thd) / float(self.sound_n + 1.)
        self.sound_n += 1.

        if numpy.mean(frame) <= self.threshold:
            self.silence_counter += 1
        else:
            self.silence_counter = 0

        if self.silence_counter > 20:
            result = False

        return result

    # Add samples to the buffer
    def add_samples(self, data):
        self.buffer = numpy.append(self.buffer, data)
        result = len(self.buffer) >= self.buffer_size
        return result

    # Pull a portion of the buffer to process
    # (pulled samples are deleted after being
    # processed
    def get_frame(self):
        window = self.buffer[:self.buffer_size]
        self.buffer = self.buffer[self.buffer_size:]
        return window

    # Adds new audio samples to the internal
    # buffer and process them
    def process(self, data):
        if self.add_samples(data):
            while len(self.buffer) >= self.buffer_size:
                # Framing
                window = self.get_frame()
                self.second_spent += 1
                if self.silence_activity_detection(window):  # speech frame
                    self.silence_segments = 0
                else:
                    self.silence_segments += 1

                if self.second_spent >= self.frame_elements: # iterating each 150 elements
                    self.second_spent = 0
                    self.time_counter += time_interval

                    if(self.silence_segments >= self.frame_elements):
                        self.silence_elements_per_second.append(1)
                        self.silence_segments = 0
                    else:
                        self.silence_elements_per_second.append(0)

def calculate_time(list, time):
    time_list =  []
    urlist_len = len(list) - 1
    time_increment = 0
    for index, value in enumerate(list):
        if (index == 0):
            if(value == 0):
                time_list.append(0)

                if(list[index + 1] == 1):
                    time_list.append(time_increment + time)

            if (value == 1 and list[index + 1] == 0):
                time_list.append(time_increment + time)
        else:
            if(index == urlist_len):
                if(value == 0):
                    time_increment += time
                    time_list.append(time_increment)
                    return time_list
            else:
                if (value == 1 and list[index + 1] == 0):
                    time_list.append(time_increment + time)

                if (value == 0 and list[index + 1] == 1 and list[index - 1] != 0):
                    time_list.append(time_increment + time)

                if (list[index + 1] == 1 and value == 0 and list[index - 1] != 1):
                    time_list.append(time_increment)

        time_increment += time

    return time_list


def get_voiced_segments(wave_file):
    rate, wav = wf.read(wave_file)
    sound_analyser = SoundAnalyser()
    sound_analyser.process(wav)
    print sound_analyser.silence_elements_per_second
    voice_segments = calculate_time(sound_analyser.silence_elements_per_second, time_interval)
    print voice_segments
    return  voice_segments