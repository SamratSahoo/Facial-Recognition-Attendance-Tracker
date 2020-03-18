import sys

from init import *
from Sheets import *
from DynamicAddition import *
import cv2
import face_recognition
import numpy as np
import os
from multiprocessing import Process, Pool
from LivenessDetection import getModel

# ================================================ Functions ===========================================================
global fullStudentNames, faceNamesKnown, encodingNames, model, video, encodingList, faceLocations, faceEncodingsKnown
global faceEncodings, faceNames, inputFrames, processThisFrame, x, file, smallFrame, rgbFrame, livenessVal, name


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


def runInParallel(*fns):
    proc = []
    for fn in fns:
        p = Process(target=fn)
        p.start()
        proc.append(p)
    for p in proc:
        p.join()


def getLivenessValue(frame, inputFrames, model):
    livenessFrame = cv2.resize(frame, (100, 100))
    livenessFrame = cv2.cvtColor(livenessFrame, cv2.COLOR_BGR2GRAY)
    inputFrames.append(livenessFrame)
    input = np.array([inputFrames[-24:]])
    input = input / 255
    input = input.reshape(1, 24, 100, 100, 1)
    pred = model.predict(input)
    return pred[0][0]


def preProcess():
    global fullStudentNames, faceNamesKnown, encodingNames, model, video, encodingList, faceLocations
    global faceEncodings, faceNames, inputFrames, processThisFrame, x, file

    fullStudentNames = loadLists("List Information/Full Student Names")  # List with full Student Names
    faceNamesKnown = loadLists("List Information/Face Names Known")  # List With Face Names
    encodingNames = loadLists("List Information/Encoding Names")  # List With encoding names
    loadDictionary("List Information/Face Names Known", faceEncodingsKnown)  # Dictionary with Encodings

    # Load Liveness Model
    model = getModel()
    model.load_weights("Model/model.h5")

    # Check if there are enough encodings
    if getFolderSize("Encodings/") != len(encodingNames):
        import EncodingModel

    # Create Webcam
    # 0 laptop webcam
    # 2 external webcam
    video = cv2.VideoCapture(0)

    # Load saved encodings for Different People
    encodingList = toList(faceEncodingsKnown)
    for x in range(0, int(len(encodingList))):
        encodingList[x] = np.load("Encodings/" + str(encodingNames[x]))

    faceLocations = []
    faceEncodings = []
    faceNames = []
    inputFrames = []
    processThisFrame = True
    x = 0
    file = open("AttendanceSheet.txt", "w+")


def optimizeWebcam(frame):
    global smallFrame, rgbFrame, livenessVal, inputFrames, model, x

    smallFrame = cv2.resize(frame, (0, 0), fx=.25, fy=.25)
    # Change Webcam to RGB
    rgbFrame = smallFrame[:, :, ::-1]
    livenessVal = getLivenessValue(frame, inputFrames, model)
    x += 1


def recognizeFaces():
    global faceLocations, faceEncodings, faceNames, blurAmount, faceEncoding, matchFound, matchIndex
    global name, faceDistances, encodingList, processThisFrame

    if processThisFrame:
        faceLocations = face_recognition.face_locations(rgbFrame, 1)
        faceEncodings = face_recognition.face_encodings(rgbFrame, faceLocations)

        # make faceNames List empty every frame; refreshes to see if person still there
        faceNames = []
        # Calculate the blur and if blur too high then do not do face detection
        blurAmount = cv2.Laplacian(frame, cv2.CV_64F).var()
        if blurAmount > 40:
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


def dynamicallyAdd(frame):
    global fullStudentNames, faceNamesKnown, encodingNames, faceEncodingsKnown, encodingList, processThisFrame, x

    if 'Not Found' in faceNames and cv2.waitKey(20) & 0xFF == ord('a'):
        runInParallel(pauseCamera(), dynamicAdd(frame))
        fullStudentNames = loadLists(
            "List Information/Full Student Names")  # List with full Student Names
        faceNamesKnown = loadLists("List Information/Face Names Known")  # List With Face Names
        encodingNames = loadLists("List Information/Encoding Names")  # List With encoding names
        loadDictionary("List Information/Face Names Known",
                       faceEncodingsKnown)  # Dictionary with Encodings

        if getFolderSize("Encodings/") != len(encodingNames):
            import EncodingModel

        encodingList = toList(faceEncodingsKnown)
        for x in range(0, int(len(encodingList))):
            encodingList[x] = np.load("Encodings/" + str(encodingNames[x]))

    processThisFrame = x % 3 == 0


def writeOnStream(frame):
    global faceLocations, faceNames, blurAmount, name

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
        blurAmount = cv2.Laplacian(frame, cv2.CV_64F).var()
        if livenessVal > 0.80:
            if blurAmount > 40:
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
        else:
            cv2.putText(frame, "WARNING: SPOOF DETECTED", (100, 75), font, 1.0, (0, 0, 255), 2)


def writeToFile():
    global livenessVal, faceNamesKnown, fullStudentNames

    if livenessVal > .80:
        # Write name in file Once only
        for x in range(0, len(faceNamesKnown)):
            checkIfHere(name, faceNamesKnown[x])

    # Commented out so frame doesnt lag like crazy; Uncomment for Google Sheets though
    # for x in range(0, len(fullStudentNames)):
    #     if name in fullStudentNames[x]:
    #         updatePresentPerson(fullStudentNames[x])


if __name__ == '__main__':
    preProcess()
    while True:
        try:
            # Open Webcam + Optimize Webcam
            ret, frame = video.read()
            optimizeWebcam(frame)
            recognizeFaces()
            dynamicallyAdd(frame)
            writeOnStream(frame)
            writeToFile()
            cv2.imshow('Frame', frame)

            # If q is pressed, exit loop
            if cv2.waitKey(20) & 0xFF == ord('q'):
                break

        except Exception as e:
            exceptionType, exceptionObject, exceptionThrowback = sys.exc_info()
            fileName = os.path.split(exceptionThrowback.tb_frame.f_code.co_filename)[1]
            print(exceptionType, fileName, exceptionThrowback.tb_lineno)
            print(e)

# ============================================== Post Program ==========================================================
# Upon exiting while loop, close web cam
    video.release()
    cv2.destroyAllWindows()

# Uncomment for Google Sheets
# markAbsentUnmarked()
