from init import *
from Sheets import *
from DynamicAddition import *
import cv2
import face_recognition
import numpy as np
import os


# ================================================ Functions ===========================================================

# Method to make sure output to file only occurs once
def checkIfHere(name, nameToCheck):
    if name is nameToCheck:
        with open("AttendanceSheet.txt", 'r') as f:
            if nameToCheck in f.read():
                pass
            else:
                with open("AttendanceSheet.txt", 'a') as f2:
                    f2.write(name + "\n")
                    f2.close()


# Method to get amount of files in a certain folder
def getFolderSize(folderName):
    fileList = os.listdir(folderName)
    numberFiles = len(fileList)
    return numberFiles


# Method to adjust to a certain brightness
def adjustBrightness(img):
    # Converts frame from RGB to HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # Splits HSV type into 3 different arrays
    h, s, v = cv2.split(hsv)
    # Calculates image's average brightness
    averageBrightness = np.sum(v) / np.size(v)
    # Set minimum brightness
    brightnessThreshold = 125
    # Calculate how much to increase the brightness
    brightnessIncrease = brightnessThreshold - int(averageBrightness)
    # See if average brightness exceeds the threshold
    if averageBrightness < brightnessThreshold:
        # Increases brightness
        lim = 255 - brightnessIncrease
        v[v > lim] = 255
        v[v <= lim] += brightnessIncrease
    # Merge the HSV values back together
    finalHSV = cv2.merge((h, s, v))
    # Redetermine image value & Return Image
    img = cv2.cvtColor(finalHSV, cv2.COLOR_HSV2BGR)
    return img


def toList(dictionary):
    listToReturn = list(dictionary.values())
    index = int(len(listToReturn))
    listToReturn = listToReturn[:index]
    return listToReturn


def loadLists(textFile):
    with open(textFile) as file:
        list = file.readlines()
        file.close()
        list = [x[:-1] for x in list]
    return list


def loadDictionary(file, dictionary):
    with open(file, "rt") as f:
        for line in f.readlines():
            dictionary[line.strip()] = None

# ================================================ Set Up ==============================================================

# Convert Txt Files to Lists
fullStudentNames = loadLists("List Information/Full Student Names")  # List with full Student Names
faceNamesKnown = loadLists("List Information/Face Names Known")  # List With Face Names
encodingNames = loadLists("List Information/Encoding Names")  # List With encoding names
loadDictionary("List Information/Full Student Names", People)  # Dictionary with people objects
loadDictionary("List Information/Face Names Known", faceEncodingsKnown)  # Dictionary with Encodings

# Check if there are enough encodings
if getFolderSize("Encodings/") != len(encodingNames):
    pass

# Create Webcam
# 0 laptop webcam
# 2 external webcam
video = cv2.VideoCapture(0)

# Load saved encodings for Different People
encodingList = toList(faceEncodingsKnown)
for x in range(0, int(len(encodingList))):
    encodingList[x] = np.load("Encodings/" + str(encodingNames[x]))

# Load Object Information
peopleList = toList(People)
for x in range(0, len(peopleList)):
    peopleList[x] = Person(faceNamesKnown[x], fullStudentNames[x], encoding=encodingList[x],
                           image=None, imagePath=None, encodingPath=None)

faceLocations = []
faceEncodings = []
faceNames = []
processThisFrame = True
file = open("AttendanceSheet.txt", "w+")
# ============================================== Core Program ==========================================================

while True:
    try:
        # ============================================== Webcam Optimization ===========================================
        # Open Webcam + Optimize Webcam
        ret, frame = video.read()
        smallFrame = cv2.resize(frame, (0, 0), fx=.25, fy=.25)

        # Change Webcam to RGB
        rgbFrame = smallFrame[:, :, ::-1]
        # ============================================== Facial Recognition ============================================

        # Find face locations and then do facial recognition to it
        if processThisFrame:
            faceLocations = face_recognition.face_locations(rgbFrame, 2, "hog")
            faceEncodings = face_recognition.face_encodings(rgbFrame, faceLocations)

            # make faceNames List empty every frame; refreshes to see if person still there
            faceNames = []
            # Calculate the blur and if blur too high then do not do face detection
            blurAmount = cv2.Laplacian(frame, cv2.CV_64F).var()
            if blurAmount > 125:
                # Cycle through face encodings to find a match
                for faceEncoding in faceEncodings:
                    matchFound = face_recognition.compare_faces(encodingList, faceEncoding, 0.5)
                    name = "Not Found"

                    # See how similar or different the faces are
                    faceDistances = face_recognition.face_distance(encodingList, faceEncoding)
                    # whichever one has a lower variance, take the minimum of that
                    matchIndex = np.argmin(faceDistances)
                    if matchFound[matchIndex]:
                        name = faceNamesKnown[matchIndex]

                    # Add names to faceNames list once found
                    faceNames.append(name)

        # ============================================== Dynamic Addition ==============================================
        #             if name == 'Not Found':
        #                 pauseCamera()
        #                 takePicture()
        #                 encodeFace()

        processThisFrame = not processThisFrame
        # ============================================== Write on Stream ===============================================

        for (top, right, bottom, left), name in zip(faceLocations, faceNames):
            # scaling again to correct for previous scaling
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a Rectangle
            cv2.rectangle(frame, (left, top), (right, bottom), (255, 0, 0), 2)

            # Draw a label with a name
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (255, 0, 0), cv2.FILLED)

            # Set label font + draw Text
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

            # Write name in file Once only
            for x in range(0, len(faceNamesKnown)):
                checkIfHere(name, faceNamesKnown[x])

            for x in range(0, len(fullStudentNames)):
                if name in fullStudentNames[x]:
                    updatePresentPerson(fullStudentNames[x])

        cv2.imshow('Frame', frame)

        # If q is pressed, exit loop
        if cv2.waitKey(20) & 0xFF == ord('q'):
            break

    except Exception as e:
        print(e)

# ============================================== Post Program ==========================================================
# Upon exiting while loop, close web cam
video.release()
cv2.destroyAllWindows()
markAbsentUnmarked()
