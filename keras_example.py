# demonstrates an of a neural network controlling a game

import gamepy
import numpy as np
from gamepy import press_key, release_key
from keras.models import load_model
from keras.preprocessing.image import img_to_array, load_img

model = load_model('./Burnout/Models/inception_model.h5')
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

###################################################################################################
# We first create a function that will be fed to our KeyController class.
# This function will take the screen as an input, and output a prediction of which key to press.
# The input screen is fed through to a neural network, which generates our prediction.
###################################################################################################

def predict_key(img):
    """Feeds an image to a neural network. Maps the neural net's prediction to
    a key press.
    
    Params
    ------
    
    img: opencv image
        Image from which a key-press prediction should be made"""
    # preprocess image
    img = img_to_array(img)/255.

    if img.shape[-1] == 1:
        #last channel is wrong size
        new_img = np.zeros([*img.shape[0:2], 3])
        for i in range(3):
            new_img[:,:,i] = img[:,:,0]
        img = new_img
        del new_img

    # loads a mask for removing unwanted parts from the image 
    # (in this case, song titles and speedometer)
    # mask = load_img('C:/Data/Games/Burnout/processed/mask.png')
    # img = img*mask

    img = img.reshape(1, *img.shape)
    
    # predict the key press to be made
    key = model.predict(img)[0].argmax()
    print(key)
    
    # map the prediction to an actual keystroke
    if key == 0:
        # fw
        press_key('up')
        release_key('left')
        release_key('right')
        release_key('down')
    elif key == 1:
        # fr
        press_key('up')
        release_key('left')
        press_key('right')
        release_key('down')
    elif key == 2:
        # rt
        release_key('up')
        release_key('left')
        press_key('right')
        release_key('down')
    elif key == 3:
        # br
        release_key('up')
        release_key('left')
        press_key('right')
        press_key('down')
    elif key == 4:
        # bw
        release_key('up')
        release_key('left')
        release_key('right')
        press_key('down')
    elif key == 5:
        # bl
        release_key('up')
        press_key('left')
        release_key('right')
        press_key('down')
    elif key == 6:
        # lt
        release_key('up')
        press_key('left')
        release_key('right')
        release_key('down')
    elif key == 7:
        # fl
        press_key('up')
        press_key('left')
        release_key('right')
        release_key('down')

###################################################################################################
# Load the keycontroller, whose input is a function that takes
# the screen as an input image and produces key_presses
###################################################################################################

controller = gamepy.KeyController(predict_key)

# activate the controller
controller.control(height=299, grayscale=False)
