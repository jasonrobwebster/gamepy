# gamepy

Records images and keystrokes during gameplay for use in supervised learning projects. Associates each image of gameplay with a particular keystroke in a csv file.

# Dependancies

* numpy
* pynput

# Usage

The file `record.py` gives an example of setting up a recording session. The `Recorder` class captures the screen as an image and associates each image with a monitored key stroke. This produces data that could train a neural network to create a self driving car. The `keras_example.py` file gives an example of loading such a model that can then be used in conjuction with the `KeyController` class to produce a self driving car in a simulated gaming environment.
