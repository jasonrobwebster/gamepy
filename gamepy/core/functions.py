# utility functions

from pynput.keyboard import Key, KeyCode

__all__ = [
    'string_to_key',
    'key_to_string'
]

def string_to_key(string):
    if not isinstance(string, str):
        if isinstance(string, Key):
            return string
        raise ValueError('Input must be of type string, got %s' %string)
    
    if len(string) == 1:
        return KeyCode.from_char(string)

    if hasattr(Key, string):
            return getattr(Key, string)
    else:
        return ValueError('Input string has no matching key, got %s' %string)

def key_to_string(key):
    if isinstance(key, Key):
        return key.name
    elif isinstance(key, KeyCode):
        return str(key)
    else:
        raise ValueError('Input must be of type Key or KeyCode, got %s' %key)
