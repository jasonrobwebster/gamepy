"""
Handles key profiles.
"""
from pynput.keyboard import Key

class KeyProfile:
    """
    Class that controls key profiles.

    params:
        play_keys: list of keys
        pause_keys: list of keys that cause a pause
        terminate_keys: list keys that cause a terminate
    """

    def __init__(self, play_keys, pause_keys, terminate_keys, start_keys):
        self.play_keys = play_keys
        self.pause_keys = pause_keys
        self.terminate_keys = terminate_keys
        self.start_keys = start_keys

    @property
    def play_keys(self):
        """List of keys that indicate a game input"""
        return self.__play_keys.copy()

    @ property
    def pause_keys(self):
        """List of keys that indicate a pause input"""
        return self.__pause_keys.copy()

    @property
    def terminate_keys(self):
        return self.__terminate_keys.copy()

    @property
    def start_keys(self):
        return self.__start_keys.copy()

    @play_keys.setter
    def play_keys(self, play_keys):
        """List of keys that indicate a terminate input"""
        if not isinstance(play_keys, list):
            raise TypeError('Play keys must be a list')
        for key in play_keys:
            if not isinstance(key, Key):
                raise AssertionError('Wrong key in play keys')
        self.__play_keys = play_keys

    @pause_keys.setter
    def pause_keys(self, pause_keys):
        if not isinstance(pause_keys, list):
            raise TypeError('Pause keys must be a list')
        for key in pause_keys:
            if not isinstance(key, Key):
                raise AssertionError('Wrong key in pause keys')
        self.__pause_keys = pause_keys

    @terminate_keys.setter
    def terminate_keys(self, terminate_keys):
        if not isinstance(terminate_keys, list):
            raise TypeError('Terminate keys must be a list')
        for key in terminate_keys:
            if not isinstance(key, Key):
                raise AssertionError('Wrong key in terminate keys')
        self.__terminate_keys = terminate_keys

    @start_keys.setter
    def start_keys(self, start_keys):
        if not isinstance(start_keys, list):
            raise TypeError('Start keys must be a list')
        for key in start_keys:
            if not isinstance(key, Key):
                raise AssertionError('Wrong key in start keys')
        self.__start_keys = start_keys
        