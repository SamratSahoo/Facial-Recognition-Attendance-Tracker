import numpy as np
import keras
from keras.models import model_from_json
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv3D, MaxPooling3D
from keras import backend as K


def getModel():
    model = Sequential()
    model.add(Conv3D(32, kernel_size=(3, 3, 3),
                     activation='relu',
                     input_shape=(24, 100, 100, 1)))
    model.add(Conv3D(64, (3, 3, 3), activation='relu'))
    model.add(MaxPooling3D(pool_size=(2, 2, 2)))
    model.add(Conv3D(64, (3, 3, 3), activation='relu'))
    model.add(MaxPooling3D(pool_size=(2, 2, 2)))
    model.add(Conv3D(64, (3, 3, 3), activation='relu'))
    model.add(MaxPooling3D(pool_size=(2, 2, 2)))
    model.add(Dropout(0.25))
    model.add(Flatten())
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(2, activation='softmax'))

    return model

def getModelPred():
    model = getModel()
    model.load_weights("Model/model.h5")
    return model