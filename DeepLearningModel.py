# THIS FILE IN PROGRESS
from keras_preprocessing.image import load_img, img_to_array, array_to_img
from keras.applications.resnet50 import ResNet50
from PIL import Image
from keras.layers import Dense, Conv2D
import numpy as np
import os
from init import faceEncodingsKnown, faceNamesKnown, encodingNames

model = ResNet50(weights='imagenet')
for filename in os.listdir("People/" + faceNamesKnown):
    fileAmount = len(next(os.walk("People/" + faceNamesKnown)))
    for fileNum in range(0, fileAmount - 1):
        imageProcessed = load_img("People/" + faceNamesKnown[x] + "/" + str(fileNum) + ".jpg")
        imageArray = img_to_array(imageProcessed)
