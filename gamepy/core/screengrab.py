# Grabs, processes, and saves an image from the screen

import os
from PIL import Image, ImageGrab

__all__ = [
    'save_screen'
]

def preprocess(image, width=None, height=None, grayscale=True):
    """
    Preprocesses an image by scaling it to the given width and height.
    If only the width or height is given, will scale the image to maintain
    the aspect ratio.
    
    Params
    ------
    
    width: int (optional)
        The width of the final image.
        
    height: int (optional)
        The height of the final image
    
    grayscale: Boolean (optional)
        Whether to convert the image to grayscale. Default is True.
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


    if (w != width) and (h != height):
        image = image.resize(size=(width, height))


    # convert the image to grayscale
    if grayscale:
        image = image.convert(mode='L')

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
    
    Params
    ------
    
    process: Boolean
        preprocesses the image before saving
        
    bbox: tuple (left, top, width, height) 
        bounding box of the screen to save
        
    kwargs: keyword arguments
        passed to preprocess function, can include width, height, and grayscale
    """
    image = grab_image(process, bbox, **kwargs)

    if file is not None:
        base, name = os.path.split(file)
        if os.path.exists(base) is False:
            os.makedirs(base)
        image.save(file)

    return image
