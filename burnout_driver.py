import gamepy
import numpy as np
from gamepy import press_key, release_key
from keras.models import load_model
from keras.preprocessing.image import img_to_array, load_img

model = load_model('./Burnout/Models/vgg_model.h5')
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
        Image from which a key-press prediction should be made
    """
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
    
    # map the prediction to a keystroke
    if key == 0:
        # up
        press_key('up')
        release_key('left')
        release_key('right')
        release_key('down')
    elif key == 1:
        # up left
        press_key('up')
        press_key('left')
        release_key('right')
        release_key('down')
    elif key == 2:
        # left
        release_key('up')
        press_key('left')
        release_key('right')
        release_key('down')
    elif key == 3:
        # down left
        release_key('up')
        press_key('left')
        release_key('right')
        press_key('down')
    elif key == 4:
        # down
        release_key('up')
        release_key('left')
        release_key('right')
        press_key('down')
    elif key == 5:
        # down right
        release_key('up')
        release_key('left')
        press_key('right')
        press_key('down')
    elif key == 6:
        # right
        release_key('up')
        release_key('left')
        press_key('right')
        release_key('down')
    elif key == 7:
        # up right
        press_key('up')
        release_key('left')
        press_key('right')
        release_key('down')
    elif key == 8:
        # no key press
        release_key('up')
        release_key('left')
        release_key('right')
        release_key('down')

###################################################################################################
# Load the keycontroller, whose input is a function that takes
# the screen as an input image and produces key_presses
###################################################################################################

start_keys='home'
pause_keys='pause'
terminate_keys='end'

controller = gamepy.KeyController(predict_key)
controller.set_control_keys(start_keys=start_keys, pause_keys=pause_keys, terminate_keys=terminate_keys)

print('Press %s to start the controller, %s to pause the controller, and %s to terminate the controller.' %(str(start_keys), str(pause_keys), str(terminate_keys)))

# activate the controller
controller.control(height=299, grayscale=False)