import os
import cv2
import face_recognition
import numpy as np
import argparse
import keyboard


# Load Cascade Classifier
faceCascade = cv2.CascadeClassifier('Cascades/data/haarcascade_frontalface_alt.xml')

# Create Webcam
video = cv2.VideoCapture(0)

# Encoding Image for Samrat Sahoo
samratImage = face_recognition.load_image_file("samrat.jpg")
samratEncoding = face_recognition.face_encodings(samratImage)[0]

# Encoding Image for Caitlin Fukumoto
caitlinImage = face_recognition.load_image_file("caitlin.jpg")
caitlinEncoding = face_recognition.face_encodings(caitlinImage)[0]

# List For Face Encodings
faceEncodingsKnown = [
    samratEncoding,
    caitlinEncoding
]

# List For Face Names
faceNamesKnown = [
    "Samrat",
    "Caitlin"
]

faceLocations = []
faceEncodings = []
faceNames = []
processThisFrame = True
samratCounter = 0
caitlinCounter = 0

while True:
    # Open Webcam + Optimize Webcam
    ret, frame = video.read()
    smallFrame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Change Webcam to RGB
    rgbFrame = smallFrame[:, :, ::-1]

    # Find face locations and then do facial recognition to it
    if processThisFrame:
        faceLocations = face_recognition.face_locations(rgbFrame)
        faceEncodings = face_recognition.face_encodings(rgbFrame, faceLocations)

        # make faceNames List empty every frame; refreshes to see if person still there
        faceNames = []

        # Cycle through face encodings to find a match
        for faceEncoding in faceEncodings:
            matchFound = face_recognition.compare_faces(faceEncodingsKnown, faceEncoding)
            name = "Not Found"

            faceDistances = face_recognition.face_distance(faceEncodingsKnown, faceEncoding)
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

        # Display name in console Once only
        if samratCounter == 0 and name is 'Samrat':
            print(name)
            samratCounter = samratCounter + 1

        if caitlinCounter == 0 and name is 'Caitlin':
            print(name)
            caitlinCounter = caitlinCounter + 1


    # Show Frame
    cv2.imshow('frame', frame)

    # If q is pressed, exit loop
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

# Upon exiting while loop, close web cam
video.release()



