import cv2
import os
import numpy as np
from PIL import Image
import pickle


# Make directories universal
directory = os.path.dirname(os.path.abspath(__file__))
imageDirectory = os.path.join(directory, "images")

# Import Classifiers + Pre - Trained Models
faceCascade = cv2.CascadeClassifier('Cascades/data/haarcascade_frontalface_alt2.xml')
faceRecognizer = cv2.face.LBPHFaceRecognizer_create()

currentId = 0
labelIds = {}
xTrain = []
yLabels = []

for root, dirs, files in os.walk(imageDirectory):
    for file in files:
        if file.endswith("png") or file.endswith("jpg"):
            path = os.path.join(root, file)

            # Format the label by removing spaces and putting dash and lower casing
            label = os.path.basename(root).replace(" ", "-").lower()

            if label not in labelIds:
                labelIds[label] = currentId
                currentId+=1
            Id = labelIds[label]

            # Convert Image into grayscale
            pilImage = Image.open(path).convert("L")

            # Make image into Array
            size = (550, 550)
            finalImage = pilImage.resize(size, Image.ANTIALIAS)
            imageArray = np.array(finalImage, "uint8")

            # Face Detection in Image
            faces = faceCascade.detectMultiScale(imageArray, scaleFactor=1.5, minNeighbors=5)
            for (x, y, w, h) in faces:
                roiGray = imageArray[y:y+h, x:x+h]
                xTrain.append(roiGray)
                yLabels.append(Id)

with open("labels.picle", 'wb') as f:
    pickle.dump(labelIds, f)

faceRecognizer.train(xTrain, np.array(yLabels))
faceRecognizer.save("trainner.yml")