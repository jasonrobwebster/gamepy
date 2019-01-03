import os
import numpy as np
import pandas as pd

from collections import Counter

from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split

from burnout_utils import press_to_one_hot
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img

from keras.models import Model, save_model
from keras.layers import Dense, Flatten, Input, Conv2D, MaxPooling2D, Dropout, BatchNormalization
from keras.applications import InceptionV3


###################################################################################################
# MODEL DEFINITION
###################################################################################################

x = Input(shape=(299,532,3), name='Input')
## block1
block1_conv1 = Conv2D(32, (3,3), strides=2, padding='same', activation='relu', name='block1_conv1')(x)
block1_conv2 = Conv2D(32, (3,3), strides=1, padding='same', activation='relu', name='block1_conv2')(block1_conv1)
block1_pool = MaxPooling2D(pool_size=(3,3), name='block1_pool')(block1_conv2)
block1_drop = Dropout(0.2, name='block1_drop')(block1_pool)
## block2
block2_conv1 = Conv2D(32, (3,3), strides=1, padding='same', activation='relu', name='block2_conv1')(block1_drop)
block2_conv2 = Conv2D(32, (3,3), strides=1, padding='same', activation='relu', name='block2_conv2')(block2_conv1)
block2_pool = MaxPooling2D(pool_size=(2,2), name='block2_pool')(block2_conv2)
block2_drop = Dropout(0.2, name='block2_drop')(block2_pool)
## block3
block3_conv1 = Conv2D(32, (3,3), strides=1, padding='same', activation='relu', name='block3_conv1')(block2_drop)
block3_conv2 = Conv2D(32, (3,3), strides=1, padding='same', activation='relu', name='block3_conv2')(block3_conv1)
block3_pool = MaxPooling2D(pool_size=(2,2), name='block3_pool')(block3_conv2)
block3_drop = Dropout(0.2, name='block3_drop')(block3_pool)
## block4
block4_conv1 = Conv2D(32, (3,3), strides=1, padding='same', activation='relu', name='block4_conv1')(block3_drop)
block4_conv2 = Conv2D(32, (3,3), strides=1, padding='same', activation='relu', name='block4_conv2')(block4_conv1)
block4_pool = MaxPooling2D(pool_size=(2,2), name='block4_pool')(block4_conv2)
block4_drop = Dropout(0.2, name='block4_drop')(block4_pool)
## FC
FC_flatten = Flatten(name='FC_flatten')(block4_drop)
## FC1
FC1_dense = Dense(1024, activation='relu', name='FC1_dense')(FC_flatten)
FC1_norm = BatchNormalization(name='FC1_norm')(FC1_dense)
FC1_drop = Dropout(0.2, name='FC1_drop')(FC1_norm)
## FC2
FC2_dense = Dense(1024, activation='relu', name='FC2_dense')(FC1_drop)
FC2_norm = BatchNormalization(name='FC2_norm')(FC2_dense)
FC2_drop = Dropout(0.2, name='FC2_drop')(FC2_norm)
## FC3
FC3_dense = Dense(512, activation='relu', name='FC3_dense')(FC2_drop)
FC3_norm = BatchNormalization(name='FC3_norm')(FC3_dense)
FC3_drop = Dropout(0.2, name='FC3_drop')(FC3_norm)
## Output
FC4_output = Dense(9, activation='softmax', name='FC4_output')(FC3_drop)

model = Model(x, FC4_output)
model.compile(optimizer='Adam', loss='categorical_crossentropy', metrics=['accuracy'])

print(model.summary())


###################################################################################################
# TRAINING
###################################################################################################

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
y = np.zeros([data_length, 9])

# convert the key strokes to one hot vectors
for i, key_press in enumerate(key_presses):
    y[i]= press_to_one_hot(key_press)

# the data highly favors going forward, or pressing "up"
# to combat this, we duplicate the data that is not going forward
# until it is more or less uniform

press_counts = Counter(str(press) for press in y)
max_counts = press_counts.most_common()[0][1]

# we won't duplicate excessively small data samples, in this case, 
# any keystroke recorded less than 1000 times is not duplicated

min_counts = 1000
i = 0

while i < len(y):
    press = y[i]
    count = press_counts[str(press)]
    if count < max_counts and count > min_counts:
        x = np.append(x, [x[i]], axis=0)
        y = np.append(y, [press], axis=0)
        press_counts[str(press)] += 1
    i += 1

# to properly train our model without causing memory issues, we use a 
# a data generator, and the fit_generator method for our keras models
# we also shuffle our data and create a 10% validation sample

x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=0.1
)

image_gen = ImageDataGenerator(
    rotation_range=10, 
    width_shift_range=0.02,
    height_shift_range=0.02,
    shear_range=0.01,
    zoom_range=0.01
    )

def data_generator(x, y, batch_size = 32, randomize=False):
    assert len(x) == len(y)

    batch_images = np.zeros((batch_size, 299, 532, 3))
    batch_labels = np.zeros((batch_size, 9))

    idx = 0 # dummy variable to keep track of position in data

    while True:
        for i in range(batch_size):
            # load the image
            sample_idx = (idx + i) % len(x)
            image = load_img(x[sample_idx])
            image = img_to_array(image) / 255.

            if randomize:
                image = image_gen.random_transform(image)

            batch_images[i] = image
            batch_labels[i] = y[sample_idx]

        idx += batch_size

        yield (batch_images, batch_labels)

# we can now train our model

batch_size = 64
steps_per_epoch = len(x_train)//batch_size
validation_steps = len(x_test)//batch_size

train_gen = data_generator(x_train, y_train, batch_size=batch_size)
test_gen = data_generator(x_test, y_test, batch_size=batch_size)

model.fit_generator(
    generator = train_gen,
    steps_per_epoch = steps_per_epoch,
    epochs = 10,
    validation_data = test_gen,
    validation_steps=validation_steps,
)


###################################################################################################
# SAVING
###################################################################################################

if not os.path.exists('./Burnout/Models/'):
    os.makedirs('./Burnout/Models/')

model.save('./Burnout/Models/vgg_model.h5')