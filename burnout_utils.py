import numpy as np

def press_to_one_hot(key_press):
    """Maps a key prediction to a one hot vector"""
    key_press = np.asarray(key_press)
    out = np.zeros(9)

    if key_press[0] == 1:
        # up
        if key_press[1] == 1:
            # up left
            out[1] = 1
        elif key_press[-1] == 1:
            # up right
            out[7] = 1
        else:
            # only up
            out[0] = 1
    elif key_press[2] == 1:
        # down
        if key_press[1] == 1:
            # down left
            out[3] = 1
        elif key_press[-1] == 1:
            # down right
            out[5] = 1
        else:
            # only down
            out[4] = 1
    elif key_press[1] == 1:
        # left
        out[2] = 1
    elif key_press[-1] == 1:
        # right
        out[6] = 1
    else:
        # no key
        out[-1] = 1

    return out