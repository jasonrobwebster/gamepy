import os
import numpy as np
import pandas as pd

from burnout_utils import press_to_one_hot
#from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img

base_path = './Burnout/'
file_name = 'record.csv'
data_path = os.path.join(base_path, file_name)

data = pd.read_csv(data_path)

key_names = data.columns.values[1:]
key_presses = data[key_names].values
directories = data['Directory'].values

# store the images as "x" and the predictions as "y"
# training to find p(y|x)

data_length = len(directories)
x = directories # stored as the directories until needed to save memory
y = np.zeros([data_length, 8])

for i, key_press in enumerate(key_presses):
    y[i]= press_to_one_hot(key_press)
