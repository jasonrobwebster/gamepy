"""
Records the screen in a given number of fixed intervals until terminated.
"""

import csv
import os
import numpy as np
from datetime import datetime
from .grab import save_screen
from keys import KeyRecorder
from pynput.keyboard import Key

class Recorder:
    """
    Recorder object. Records the screen.
    """
    recorders = 0

    def __init__(self):
        self.paused = False
        self.started = False
        self.terminate = False
        self.recorders += 1
        # Just make a basic profile for burnout, change this later
        play_keys = [Key.up, Key.right, Key.down, Key.left]
        pause_keys = [Key.pause]
        terminate_keys = [Key.end]
        start_keys = [Key.home]
        self.key_recorder = KeyRecorder(play_keys, pause_keys, terminate_keys, start_keys)

    def record(self, file, csv_name = 'record.csv', wait_time=1/30, **kwargs):
        """
        Records the screen in intervals given by wait_time \n\n

        params: \n
            file: File path \n
            wait_time: Number of seconds between each screen capture \n
            kwargs: kwargs to pass to save_screen \n
                process: whether to resize and recolor the image (True) \n
                bbox: [left, top, right, bottom] box defining the area of screen to grab (None) \n
                width: width of final image in pixels (800) \n
                height: height of final image in pixels (None) \n
                grayscale: whether to turn the image into a BW image (True) \n
        """
        base, name = os.path.split(file)
        print(base,name)
        if not os.path.exists(base):
            os.makedirs(base)
        image_name, fmt = name.split('.')
        index = 1

        csv_dir = base + '/' + csv_name
        if os.path.exists(csv_dir):
            os.remove(csv_dir) #clears the old recording

        csv_file = open(csv_dir, 'a', newline='')
        csv_writer = csv.writer(csv_file)

        last_time = datetime.now()
        self.key_recorder.start()

        while self.terminate is False:
            time = datetime.now()
            interval = time - last_time
            secs = interval.seconds + interval.microseconds * 1e-6
            if self.key_recorder.is_started == True and self.started == False:
                self.started = True
                print('Starting recording...')
            if self.key_recorder.is_terminated == True:
                self.terminate = True
                print('Terminating recording...')

            if secs > wait_time and self.paused is False and self.started is True:
                last_time = datetime.now()
                if np.sum(self.key_recorder.play_keys) > 0:
                    file_dir = base + '/' + image_name + str(index) + '.' + fmt
                    save_screen(file_dir, **kwargs)
                    csv_writer.writerow([file_dir, str(self.key_recorder.play_keys)])
                    index += 1
                    
        csv_file.close()
        self.key_recorder.stop()
