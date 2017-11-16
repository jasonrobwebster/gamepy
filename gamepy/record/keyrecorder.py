"""
Records the screen in a given number of fixed intervals until terminated.
"""

import os
import csv
import numpy as np
from datetime import datetime
from time import sleep
from gamepy.core import save_screen, string_to_key, key_to_string
from pynput.keyboard import Key, KeyCode
from pynput import keyboard
from gamepy.core import KeyProfile

__all__=[
    'KeyRecorder',
    'Recorder'
]

class KeyRecorder:
    """
    Class that controls key recording
    """
    # TODO: Make property names clearer
    @property
    def listener(self):
        """The keyboard listener"""
        return self.__listener

    @property
    def profile(self):
        """The keyboard profile object"""
        return self.__profile

    @property
    def play_keys(self):
        """Returns a numpy array indicating the map of play keys pressed"""
        return self.__plays

    @property 
    def is_paused(self):
        """Returns a bool indicating whether a pause key is pressed"""
        test = np.sum(self.__paused)
        return test > 0

    @property 
    def is_terminated(self):
        """Returns a bool indicating whether a terminate key is pressed"""
        test = np.sum(self.__terminated)
        return test > 0

    @property
    def is_started(self):
        """Returns a bool indicating whether a start key is pressed"""
        test = np.sum(self.__started)
        return test > 0

    @property
    def running(self):
        return self.listener.running

    @listener.setter
    def listener(self, listener):
        if not isinstance(listener, keyboard.Listener):
            raise TypeError('Setting listener to wrong type')
        assert isinstance(listener, keyboard.Listener)
        self.__listener = listener

    @profile.setter
    def profile(self, profile):
        if not isinstance(profile, KeyProfile):
            raise TypeError('Setting key profile to wrong type')
        assert isinstance(profile, KeyProfile)
        self.__profile = profile

    def __init__(self, play_keys, pause_keys, terminate_keys, start_keys):
        self.__plays = np.zeros(len(play_keys), dtype=bool)
        self.__paused = np.zeros(len(pause_keys), dtype=bool)
        self.__terminated = np.zeros(len(terminate_keys), dtype=bool)
        self.__started = np.zeros(len(start_keys), dtype=bool)
        self.profile = KeyProfile(play_keys, pause_keys, terminate_keys, start_keys)
        self.listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release
        )

    def start(self):
        """Starts the listener"""
        if self.running is False:
            self.listener.start()
            self.listener.wait()
    
    def stop(self):
        """Stops the listener"""
        if self.running is True:
            self.listener.stop()
    
    def on_press(self, key_press):
        """
        On_press method for the listener
        """
        play_keys = self.profile.play_keys
        pause_keys = self.profile.pause_keys
        terminate_keys = self.profile.terminate_keys
        start_keys = self.profile.start_keys

        for index, key in enumerate(play_keys):
            if key_press == key:
                self.__plays[index] = 1

        for index, key in enumerate(pause_keys):
            if key_press == key:
                self.__paused[index] = 1
        
        for index, key in enumerate(terminate_keys):
            if key_press == key:
                self.__terminated[index] = 1

        for index, key in enumerate(start_keys):
            if key_press == key:
                self.__started[index] = 1

    def on_release(self, key_release):
        """
        On_release method for the listener
        """
        play_keys = self.profile.play_keys
        pause_keys = self.profile.pause_keys
        terminate_keys = self.profile.terminate_keys
        start_keys = self.profile.start_keys

        for index, key in enumerate(play_keys):
            if key_release == key:
                self.__plays[index] = 0

        for index, key in enumerate(pause_keys):
            if key_release == key:
                self.__paused[index] = 0
        
        for index, key in enumerate(terminate_keys):
            if key_release == key:
                self.__terminated[index] = 0

        for index, key in enumerate(start_keys):
            if key_release == key:
                self.__started[index] = 0
    
class Recorder:
    """
    Recorder object. Records the screen.
    """
    recorders = 0

    def __init__(self, play_keys, pause_keys='pause', terminate_keys='end', start_keys='home'):
        self.paused = False
        self.started = False
        self.terminate = False
        self.recorders += 1

        # turn the keys into lists
        play_keys = [play_keys] if not isinstance(play_keys, list) else play_keys
        pause_keys = [pause_keys] if not isinstance(pause_keys, list) else pause_keys
        terminate_keys = [terminate_keys] if not isinstance(terminate_keys, list) else terminate_keys
        start_keys = [start_keys] if not isinstance(start_keys, list) else start_keys

        # turn the lists into key mappings
        play_keys = list(map(string_to_key, play_keys))
        pause_keys = list(map(string_to_key, pause_keys))
        terminate_keys = list(map(string_to_key, terminate_keys))
        start_keys = list(map(string_to_key, start_keys))

        self.key_recorder = KeyRecorder(play_keys, pause_keys, terminate_keys, start_keys)

    def record(self, file, csv_name = 'record.csv', remove_old=True, wait_time=1/30, **kwargs):
        """
        Records the screen in intervals given by wait_time 

        Parameters
        ==========

        file: File path

        wait_time: Number of seconds between each screen capture.

        remove_old: Whether to remove the old csv file. Defaults to True.

        kwargs: passed to the save_screen function. 
            See the usage of save_screen for more details.
        """
        # TODO: Fix wonky way of making and creating files
        # Currently you input a "C:/.../image.png" string into the file arg
        # which then constructs the base_dir, image base name, format, etc.
        # These should all be seperate params.
        base, name = os.path.split(file)
        print(base,name)
        if not os.path.exists(base):
            os.makedirs(base)
        image_name, fmt = name.split('.')
        index = 1

        csv_dir = base + '/' + csv_name
        if os.path.exists(csv_dir) and remove_old is True:
            os.remove(csv_dir)

        csv_file = open(csv_dir, 'a', newline='')
        csv_writer = csv.writer(csv_file)

        # write the header
        play_keys = self.key_recorder.profile.play_keys
        key_names = list(map(key_to_string, play_keys))
        csv_writer.writerow(['Directory', *key_names] )

        last_time = datetime.now()
        self.key_recorder.start()

        while self.started is False:
            if self.key_recorder.is_started == True:
                self.started = True
                print('Starting recording...')

        while self.started and not self.terminate:
            time = datetime.now()
            interval = time - last_time
            secs = interval.seconds + interval.microseconds * 1e-6

            if self.key_recorder.is_paused:
                self.paused = True
                print('Pausing recording...')
                sleep(1)
            if self.key_recorder.is_terminated:
                self.terminate = True
                print('Terminating recording...')
                break

            while self.paused:
                if self.key_recorder.is_started or self.key_recorder.is_paused:
                    self.paused = False
                    print('Restarting recording...')
                    sleep(1)

            if secs > wait_time and not self.paused:
                last_time = datetime.now()
                # make the file directory and save the screen
                file_dir = base + '/' + image_name + str(index) + '.' + fmt
                save_screen(file_dir, **kwargs)
                
                # write the output
                pressed_keys = self.key_recorder.play_keys.tolist()
                csv_writer.writerow([file_dir, *pressed_keys])
                index += 1
                    
        csv_file.close()
        self.key_recorder.stop()
