
import gamepy
import numpy as np
from gamepy import press_key, release_key
from keras.models import load_model
from keras.preprocessing.image import img_to_array, load_img

model = load_model('C:/Data/Games/Burnout/models/model_vgg_v2.h5')
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

def predict_key(img):
    img = img_to_array(img)/255.

    if img.shape[2] == 1:
        #last channel is wrong size
        new_img = np.zeros([*img.shape[0:2], 3])
        for i in range(3):
            new_img[:,:,i] = img[:,:,0]
        img = new_img
        del new_img

    #load the mask
    mask = load_img('C:/Data/Games/Burnout/processed/mask.png')
    img = img*mask

    img = img.reshape(1, *img.shape)

    key = model.predict(img)[0].argmax()
    print(key)

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


controller = gamepy.KeyController(predict_key)


large_bbox = [0,200,1440,900]
controller.control(bbox=large_bbox, height=112)
