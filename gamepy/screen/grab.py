"""
Grabs, processes and save an image from the screen
"""

import os
from PIL import Image, ImageGrab

def preprocess(image, width=800, height=None, grayscale=True):
    """
    Preprocesses an image by scaling it to the correct width and height.
    """
    assert isinstance(image, Image.Image)

    w, h = (image.width, image.height)

    if width is None and height is not None:
        # preserve AR
        width = round(w/h * height)
    elif height is None and width is not None:
        # preserve AR
        height = round(h/w * width)
    elif height is None and width is None:
        # make them the image size
        width, height = (w, h)
    #end if

    if (w != width) and (h != height):
        image = image.resize(size=(width, height))
    #end if

    # convert the image to grayscale
    if grayscale:
        image = image.convert(mode='L')
    #end if
    return image


def grab_image(process=True, bbox=None, **kwargs):
    """
    Grabs an image from the screen and optionally processes it.
    Passes kwargs to preprocess function.
    """
    image = ImageGrab.grab(bbox)
    if process:
        image = preprocess(image, **kwargs)
    #end if
    return image


def save_screen(file=None, process=True, bbox=None, **kwargs):
    """
    Save the screen to the file location. Returns the image as PIL Image.
    process: preprocesses the image before saving
    bbox: (left, top, width, height) bounding box of the screen to save
    kwargs: keyword arguments for preprocess (width, height, grayscale)
    """
    image = grab_image(process, bbox, **kwargs)

    if file is not None:
        base, name = os.path.split(file)
        if os.path.exists(base) is False:
            os.makedirs(base)
        image.save(file)

    return image
