import cv2
import face_recognition
import numpy as np
import os

from init import faceNamesKnown, faceEncodingsKnown, encodingNames


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


# Method to get amounts of files in a certain folder
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


# Check if there are enough encodings
if getFolderSize("Encodings/") != len(encodingNames):
    import EncodingModel

# Create Webcam
video = cv2.VideoCapture(0)

# Load saved encodings for Different People
for x in range(0, len(faceEncodingsKnown)):
    faceEncodingsKnown[x] = np.load("Encodings/" + str(encodingNames[x]))

faceLocations = []
faceEncodings = []
faceNames = []
processThisFrame = True

file = open("AttendanceSheet.txt", "w+")

while True:
    try:
        # Open Webcam + Optimize Webcam
        ret, frame = video.read()
        smallFrame = cv2.resize(frame, (0, 0), fx=.25, fy=.25)
        smallFrame = adjustBrightness(smallFrame)
        frame = adjustBrightness(frame)

        # Change Webcam to RGB
        rgbFrame = smallFrame[:, :, ::-1]

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
                    matchFound = face_recognition.compare_faces(faceEncodingsKnown, faceEncoding, 0.5)
                    name = "Not Found"

                    # See how similar or different the faces are
                    faceDistances = face_recognition.face_distance(faceEncodingsKnown, faceEncoding)
                    # whichever one has a lower variance, take the minimum of that
                    matchIndex = np.argmin(faceDistances)
                    if matchFound[matchIndex]:
                        name = faceNamesKnown[matchIndex]

                    # Add names to faceNames list once found
                    faceNames.append(name)

        processThisFrame = not processThisFrame

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

        # Show Frame
        cv2.imshow('frame', frame)

        # If q is pressed, exit loop
        if cv2.waitKey(20) & 0xFF == ord('q'):
            break
    except Exception as e:
        print(e)

# Upon exiting while loop, close web cam
video.release()
