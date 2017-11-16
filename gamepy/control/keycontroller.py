"""
Specific class for the keras model I trained.
Very Janky, don't use
"""

from gamepy.record import KeyRecorder
from pynput.keyboard import Key
from gamepy.core import save_screen, string_to_key, key_to_string
from datetime import datetime
from time import sleep
import random

__all__ = [
    'KeyController'
]

class KeyController:
    """
    Keyboard controller class. 
    """

    def __init__(self, func, *args, **kwargs):
        if not callable(func):
            raise ValueError('Function must be callable. Got %s' %func)
        self.func = func
        self.args = args
        self.kwargs = kwargs

        self.started = False
        self.terminate = False
        self.paused = False

        play_keys = []
        pause_keys = [Key.pause]
        terminate_keys = [Key.end]
        start_keys = [Key.home]
        self.key_recorder = KeyRecorder(play_keys, pause_keys, terminate_keys, start_keys)

    def set_control_keys(self, start='home', pause='pause', terminate='end'):
        """Sets the start, pause, and terminate keys for the controller.
        
        Parameters
        ==========

        start: String, List
            The start key or list of keys
        """

        if not isinstance(start, list):
            start = [start]
        if not isinstance(pause, list):
            pause = [pause]
        if not isinstance(terminate, list):
            terminate = [terminate]

        start = list(map(string_to_key, start))
        pause = list(map(string_to_key, pause))
        terminate = list(map(string_to_key, terminate))

        self.key_recorder = KeyRecorder([], pause, terminate, start)

    
    def control(self, wait_time=1/60, **kwargs):
        last_time = datetime.now()
        self.key_recorder.start()

        print('Controller ready')

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
                print('Pausing Control...')
                sleep(1)
            if self.key_recorder.is_terminated:
                self.terminate = True
                print('Terminating Control...')
                break

            while self.paused:
                if self.key_recorder.is_started or self.key_recorder.is_paused:
                    self.paused = False
                    print('Restarting Control...')
                    sleep(1)

            if secs > wait_time and self.paused is False and self.started is True:
                last_time = datetime.now()
                img = save_screen(**kwargs)

                # call the function
                func = self.func
                args = self.args
                kwargs = self.kwargs

                func(img, *args, **kwargs)
                
        self.key_recorder.stop()

        