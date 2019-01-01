import os
import random
import numpy as np
import pandas as pd
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img

from keras.models import Model, save_model
from keras.layers import Dense, Flatten
from keras.applications import InceptionV3

# Create the model

inception = InceptionV3(include_top=False, input_shape=(299, 532, 3))
flat = Flatten(name='flatten')(inception.output)
out = Dense(8, activation='softmax', name='output')(flat)

model = Model(inception.input, out)
model.compile(optimizer='Adam', loss='categorical_crossentropy', metrics=['accuracy'])

print(model.summary())

# Train the model using the data we recorded

base_path = './Burnout/'
file_path = os.path.join(base_path, 'record.csv')

data = pd.read_csv(file_path)

data.head()

# Save the trained model

save_model(model, './Burnout/Models/inception_model.h5')