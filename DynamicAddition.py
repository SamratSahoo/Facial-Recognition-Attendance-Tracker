import TransferLearning
import cv2
import os
from EncodingModel import *

def pauseCamera():
    cv2.waitKey(-100)


class Person:

    def __init__(self, firstName, fullName, image, encoding, imagePath, encodingPath):
        self.firstName = firstName
        self.fullName = fullName
        self.image = image
        self.encoding = encoding
        self.imagePath = imagePath
        self.encodingPath = encodingPath

    def encodeFace(self):
        return encodeDirectory(self.encodingPath)

    def saveFace(self):
        os.mkdir(self.imagePath)
        cv2.imwrite(os.path.join(self.imagePath, '0.jpg'), self.image)
        cv2.imwrite(os.path.join(self.imagePath, '1.jpg'), self.image)

    def getImagePath(self):
        return '/People Images/' + str(self.name)

    def getEncodingPath(self):
        return '/Encodings/' + str(self.name).replace(" ", "") + 'Encoding.npy'

    def promptPerson(self):
        self.firstName = input("What is your first name:")
        self.fullName = self.firstName + " " + input("What is your last name:")

    def takePicture(self, frame):
        self.image = frame
