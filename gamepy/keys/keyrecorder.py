"""
Contains the core functionality for handling key recording
"""

from pynput import keyboard
import numpy as np
from .profile import KeyProfile

class KeyRecorder:
    """
    Class that controls key recording
    """
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
        self.__plays = np.zeros(len(play_keys))
        self.__paused = np.zeros(len(pause_keys))
        self.__terminated = np.zeros(len(terminate_keys))
        self.__started = np.zeros(len(start_keys))
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
