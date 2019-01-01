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



# Save the trained model

save_model(model, 'C:/Data/Games/Burnout/Models/inception_model.h5')