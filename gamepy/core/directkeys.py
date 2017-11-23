# direct inputs
# source to this solution and code:
# http://stackoverflow.com/questions/14489013/simulate-python-keypresses-for-controlling-a-game
# http://www.gamespp.com/directx/directInputKeyboardScanCodes.html
# Some code pulled from https://github.com/Sentdex/pygta5

import ctypes
import time
from pynput._util.win32 import MOUSEINPUT, KEYBDINPUT, HARDWAREINPUT, INPUT_union, INPUT
from pynput.keyboard import Key, KeyCode

__all__ = [
    'press_key',
    'release_key'
]

dk = {
    "1":            0x02,
    "2":            0x03,
    "3":            0x04,
    "4":            0x05,
    "5":            0x06,
    "6":            0x07,
    "7":            0x08,
    "8":            0x09,
    "9":            0x0A,
    "0":            0x0B,

    "NUMPAD1":      0x4F,       "NP1":      0x4F,
    "NUMPAD2":      0x50,       "NP2":      0x50,
    "NUMPAD3":      0x51,       "NP3":      0x51,
    "NUMPAD4":      0x4B,       "NP4":      0x4B,
    "NUMPAD5":      0x4C,       "NP5":      0x4C,
    "NUMPAD6":      0x4D,       "NP6":      0x4D,
    "NUMPAD7":      0x47,       "NP7":      0x47,
    "NUMPAD8":      0x48,       "NP8":      0x48,
    "NUMPAD9":      0x49,       "NP9":      0x49,
    "NUMPAD0":      0x52,       "NP0":      0x52,
    "DIVIDE":       0xB5,       "NPDV":     0xB5,
    "MULTIPLY":     0x37,       "NPM":      0x37,
    "SUBSTRACT":    0x4A,       "NPS":      0x4A,
    "ADD":          0x4E,       "NPA":      0x4E,
    "DECIMAL":      0x53,       "NPDC":     0x53,
    "NUMPADENTER":  0x9C,       "NPE":      0x9C,

    "A":            0x1E,
    "B":            0x30,
    "C":            0x2E,
    "D":            0x20,
    "E":            0x12,
    "F":            0x21,
    "G":            0x22,
    "H":            0x23,
    "I":            0x17,
    "J":            0x24,
    "K":            0x25,
    "L":            0x26,
    "M":            0x32,
    "N":            0x31,
    "O":            0x18,
    "P":            0x19,
    "Q":            0x10,
    "R":            0x13,
    "S":            0x1F,
    "T":            0x14,
    "U":            0x16,
    "V":            0x2F,
    "W":            0x11,
    "X":            0x2D,
    "Y":            0x15,
    "Z":            0x2C,

    "F1":           0x3B,
    "F2":           0x3C,
    "F3":           0x3D,
    "F4":           0x3E,
    "F5":           0x3F,
    "F6":           0x40,
    "F7":           0x41,
    "F8":           0x42,
    "F9":           0x43,
    "F10":          0x44,
    "F11":          0x57,
    "F12":          0x58,

    "UP":           0xC8,
    "LEFT":         0xCB,
    "RIGHT":        0xCD,
    "DOWN":         0xD0,

    "ESC":          0x01,
    "SPACE":        0x39,       "SPC":      0x39,
    "RETURN":       0x1C,       "ENT":      0x1C,       "ENTER":        0x1C,
    "INSERT":       0xD2,       "INS":      0xD2,
    "DELETE":       0xD3,       "DEL":      0xD3,
    "HOME":         0xC7,
    "END":          0xCF,
    "PRIOR":        0xC9,       "PGUP":     0xC9,       "PAGE_UP":      0xC9,
    "NEXT":         0xD1,       "PGDN":     0xD1,       "PAGE_DOWN":    0xD1,
    "BACK":         0x0E,       "BACKSPACE":0x0E,
    "TAB":          0x0F,
    "LCONTROL":     0x1D,       "LCTRL":    0x1D,       "CTRL_L":       0x1D,       "CTRL":         0x1D,
    "RCONTROL":     0x9D,       "RCTRL":    0x9D,       "CTRL_R":       0x9D,
    "LSHIFT":       0x2A,       "LSH":      0x2A,       "SHIFT_L":      0x2A,       "SHIFT":        0x2A,
    "RSHIFT":       0x36,       "RSH":      0x36,       "SHIFT_R":      0x36,
    "LMENU":        0x38,       "LALT":     0x38,       "ALT_L":        0x38,       "ALT":          0x38,
    "RMENU":        0xB8,       "RALT":     0xB8,       "ALT_R":        0xB8,
    "LWIN":         0xDB,
    "RWIN":         0xDC,
    "APPS":         0xDD,
    "CAPITAL":      0x3A,       "CAPS":     0x3A,       "CAPS_LOCK":    0x3A,
    "NUMLOCK":      0x45,       "NUM":      0x45,       "NUM_LOCK":     0x45,
    "SCROLL":       0x46,       "SCR":      0x46,       "SCROLL_LOCK":  0x46,

    "MINUS":        0x0C,       "MIN":      0x0C,       "-":            0x0C,
    "LBRACKET":     0x1A,       "LBR":      0x1A,       "[":            0x1A,
    "RBRACKET":     0x1B,       "RBR":      0x1B,       "]":            0x1B,
    "SEMICOLON":    0x27,       "SEM":      0x27,       ";":            0x27,
    "APOSTROPHE":   0x28,       "APO":      0x28,       "'":            0x28,
    "GRAVE":        0x29,       "GRA":      0x29,       "`":            0x29,
    "BACKSLASH":    0x2B,       "BSL":      0x2B,       "\\":           0x2B,
    "COMMA":        0x33,       "COM":      0x33,       ",":            0x33,
    "PERIOD":       0x34,       "PER":      0x34,       ".":            0x34,
    "SLASH":        0x35,       "SLA":      0x35,       "/":            0x35
}

def _press_key(hexKeyCode):
    ii_ = INPUT_union()
    ii_.ki = KEYBDINPUT( 0, hexKeyCode, 0x0008, 0)
    x = INPUT( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def _release_key(hexKeyCode):
    ii_ = INPUT_union()
    ii_.ki = KEYBDINPUT( 0, hexKeyCode, 0x0008 | 0x0002, 0)
    x = INPUT( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def press_key(key):
    """
    Creates a direct key press. 
    Allows control of a game using a keyboard input, unlike a virtual key press.

    Parameters
    ==========

    key: String, Key, KeyCode
        The key to press. Can be a string, like 'w', or a pynput Key or KeyCode.
    """
    if isinstance(key, Key):
        key = Key.name
    if isinstance(key, KeyCode):
        key = str(key)
    if not isinstance(key, str):
        raise ValueError('key must be of type str, Key or KeyCode, got %s' %key)
    
    key = key.upper()
    key_hex_code = dk.get(key)

    if key_hex_code is not None:
        _press_key(key_hex_code)
    else:
        raise ValueError('key is not a valid key, got %s' %key)

def release_key(key):
    """
    Releases a direct key press. 
    Allows control of a game using a keyboard input, unlike a virtual key press.

    Parameters
    ==========

    key: String, Key, KeyCode
        The key to press. Can be a string, like 'w', or a pynput Key or KeyCode.
    """
    if isinstance(key, Key):
        key = Key.name
    if isinstance(key, KeyCode):
        key = str(key)
    if not isinstance(key, str):
        raise ValueError('key must be of type str, Key or KeyCode, got %s' %key)
    
    key = key.upper()
    key_hex_code = dk.get(key)

    if key_hex_code is not None:
        _release_key(key_hex_code)
    else:
        raise ValueError('key is not a valid key, got %s' %key)
