"""
Specific class for the keras model I trained.
Very Janky, don't use
"""

from keys import KeyRecorder
from keras.models import load_model
from keras.preprocessing.image import img_to_array, array_to_img, load_img
import numpy as np
np.set_printoptions(precision=2, suppress=True)
from pynput.keyboard import Key
from screen.grab import save_screen
from datetime import datetime
from time import sleep
import random

class KeyController:
    """
    Janky controller class for a specific keras model
    """

    def __init__(self):
        model_dir = "C:/Data/Games/Burnout/models/model_v1.h5"
        mask_dir = "C:/Data/Games/Burnout/mask.png"

        mask = load_img(mask_dir, grayscale=True)
        mask = img_to_array(mask)/255.

        self.model = load_model(model_dir)
        self.mask = mask
        self.paused = False
        self.started = False
        self.terminate = False
        play_keys = []
        pause_keys = [Key.pause]
        terminate_keys = [Key.end]
        start_keys = [Key.home]
        self.key_recorder = KeyRecorder(play_keys, pause_keys, terminate_keys, start_keys)
    
    def control(self, wait_time=1/60, **kwargs):
        from .directkeys import PressKey, ReleaseKey, LEFT, UP, RIGHT, DOWN
        last_time = datetime.now()
        self.key_recorder.start()

        #keyboard = Controller()

        print('Controller ready')

        while self.terminate is False:
            time = datetime.now()
            interval = time - last_time
            secs = interval.seconds + interval.microseconds * 1e-6

            if self.key_recorder.is_started == True and self.started == False:
                self.started = True
                print('Starting recording...')
            if self.key_recorder.is_paused == True and self.paused == True:
                self.paused = False
                print('Unpausing recording...')
                sleep(2)
            if self.key_recorder.is_paused == True and self.paused == False:
                self.paused = True
                print('Pausing recording...')
                sleep(2)
            if self.key_recorder.is_terminated == True:
                self.terminate = True
                print('Terminating recording...')

            key_code = None

            if secs > wait_time and self.paused is False and self.started is True:
                last_time = datetime.now()

                img = save_screen(bbox=[0,200,1440,900])
                img = img_to_array(img)/255.
                img = img*self.mask

                img = img.reshape(1, 389, 800, 1)
                key_code = self.model.predict(img)[0]

            if key_code is not None and not self.paused:
                choice = np.random.choice(8, p=key_code)
                choice = np.argmax(key_code)
                mean = np.sum(np.arange(8) * key_code)
                mean2 = np.sum(np.arange(8)**2 * key_code)
                std_dev = np.sqrt(mean2-mean**2)
                print(choice, key_code, mean, std_dev, secs)
                if choice == 0:
                    # fw
                    PressKey(UP)
                    ReleaseKey(RIGHT)
                    ReleaseKey(DOWN)
                    ReleaseKey(LEFT)
                elif choice == 1:
                    # fr
                    PressKey(UP)
                    PressKey(RIGHT)
                    ReleaseKey(DOWN)
                    ReleaseKey(LEFT)
                elif choice == 2:
                    # rt
                    ReleaseKey(UP)
                    if random.randint(0,3) == 1:
                        PressKey(UP)
                    PressKey(RIGHT)
                    ReleaseKey(DOWN)
                    ReleaseKey(LEFT)
                elif choice == 3:
                    # br
                    ReleaseKey(UP)
                    PressKey(RIGHT)
                    PressKey(DOWN)
                    ReleaseKey(LEFT)
                elif choice == 4:
                    # bw
                    ReleaseKey(UP)
                    ReleaseKey(RIGHT)
                    PressKey(DOWN)
                    ReleaseKey(LEFT)
                elif choice == 5:
                    # bl
                    ReleaseKey(UP)
                    ReleaseKey(RIGHT)
                    PressKey(DOWN)
                    PressKey(LEFT)
                elif choice == 6:
                    # lt
                    ReleaseKey(UP)
                    if random.randint(0,3) == 1:
                        PressKey(UP)
                    ReleaseKey(RIGHT)
                    ReleaseKey(DOWN)
                    PressKey(LEFT)
                elif choice == 7:
                    # fl
                    PressKey(UP)
                    ReleaseKey(RIGHT)
                    ReleaseKey(DOWN)
                    PressKey(LEFT)
                
        self.key_recorder.stop()

        