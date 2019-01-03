# defines a class that feeds the screen as an input image to a function that controls a game

from gamepy.record import KeyRecorder
from pynput.keyboard import Key
from gamepy.core import save_screen, string_to_key, key_to_string
from datetime import datetime
from time import sleep, time
import random
import traceback

__all__ = [
    'KeyController'
]

class KeyController:
    """
    Keyboard controller class. 
    """

    def __init__(self, func, *args, **kwargs):
        """Keyboard controller class. Accepts as input a function 
        that takes an image of the screen as input. Typically
        a function that produces key-strokes given the state
        of the screen."""
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
        self.key_recorder = KeyRecorder(play_keys, start_keys=start_keys, pause_keys=pause_keys, terminate_keys=terminate_keys)

    def set_control_keys(self, start_keys='home', pause_keys='pause', terminate_keys='end'):
        """Sets the start, pause, and terminate keys for the controller.
        
        Parameters
        ==========

        start_keys: String, List
            The keys used to start the controller

        pause_keys: String, List
            The keys used to pause the controller
        
        terminate_keys: String, List
            The keys used to terminate the controller
        """

        if not isinstance(start_keys, list):
            start_keys = [start_keys]
        if not isinstance(pause_keys, list):
            pause_keys = [pause_keys]
        if not isinstance(terminate_keys, list):
            terminate_keys = [terminate_keys]

        start_keys = list(map(string_to_key, start_keys))
        pause_keys = list(map(string_to_key, pause_keys))
        terminate_keys = list(map(string_to_key, terminate_keys))

        self.key_recorder = KeyRecorder([], start_keys=start_keys, pause_keys=pause_keys, terminate_keys=terminate_keys)

    
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
                func_args = self.args
                func_kwargs = self.kwargs

                try:
                    func(img, *func_args, **func_kwargs)
                except:
                    traceback.print_exc()
                    self.terminate = True
                    break
                
        self.key_recorder.stop()

        
