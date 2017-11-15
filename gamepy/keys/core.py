"""Core of the keys class"""

from pynput.keyboard import Key, KeyCode

KEY_DICT = {
    "alt"       :   Key.alt,
    "alt_gr"    :   Key.alt_gr,
    "alt_l"     :   Key.alt_l,
    "alt_r"     :   Key.alt_r,
    "back"      :   Key.backspace,
    "backspace" :   Key.backspace,
    "caps_lock" :   Key.caps_lock,
    "cmd"       :   Key.cmd,
    "cmd_l"     :   Key.cmd_l,
    "cmd_r"     :   Key.cmd_r,
    "delete"    :   Key.delete,
    "end"       :   Key.end,
    "enter"     :   Key.up,
    "esc"       :   Key.esc,
    "f1"        :   Key.f1,
    "f2"        :   Key.f2,
    "f3"        :   Key.f3,
    "f4"        :   Key.f4,
    "f5"        :   Key.f5,
    "f6"        :   Key.f6,
    "f7"        :   Key.f7,
    "f8"        :   Key.f8,
    "f9"        :   Key.f9,
    "f10"       :   Key.f10,
    "f11"       :   Key.f11,
    "f12"       :   Key.f12,
    "home"      :   Key.home,
    "insert"    :   Key.insert,
    "ins"       :   Key.insert,
    "menu"      :   Key.menu,
    "num_lock"  :   Key.num_lock,
    "page_down" :   Key.page_down,
    "page_up"   :   Key.page_up,
    "pause"     :   Key.pause,
    "print_screen": Key.print_screen,
    "prtscn"    :   Key.print_screen,
    "scroll_lock":  Key.scroll_lock,
    "scrlk"     :   Key.scroll_lock,
    "shift"     :   Key.shift,
    "shift_l"   :   Key.shift_l,
    "shift_r"   :   Key.shift_r,
    "space"     :   Key.space,
    "tab"       :   Key.tab,

    "up"        :   Key.up,
    "down"      :   Key.down,
    "left"      :   Key.left,
    "right"     :   Key.right
}

def return_key(key_code):
    assert isinstance(key_code, str)
    key_code = key_code.lower()

    if key_code in KEY_DICT.keys():
        return KEY_DICT[key_code]
    else:
        return
         