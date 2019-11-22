import cv2
import face_recognition
import numpy as np
import os


def encodeFace(imageDirectory):
    # Load Images
    image = face_recognition.load_image_file(imageDirectory)
    # Encode Images
    encoding = face_recognition.face_encodings(image)[0]
    return encoding


def encodeDirectory(directoryName):
    # Create list for all encodings
    allEncodings = []
    # Go through directory of files
    for filename in os.listdir("People/" + directoryName):
        # Get amount of files in directory
        fileAmount = len(next(os.walk("People/" + directoryName)))
        if filename.endswith(".jpg"):
            # iterate through files in directory
            for fileNum in range(0, fileAmount - 1):
                # Add encodings to list
                allEncodings.append(encodeFace("People/" + directoryName + "/" + str(fileNum) + ".jpg"))
    # Turn length of list to prevent integer division
    listLength = len(allEncodings) * 1.0
    # Return average of encoded arrays array
    return sum(allEncodings) / listLength


def checkIfHere(name, nameToCheck):
    if name is nameToCheck:
        with open("AttendanceSheet.txt", 'r') as f:
            if nameToCheck in f.read():
                pass
            else:
                with open("AttendanceSheet.txt", 'w') as f2:
                    f2.write(name + "\n")


# Create Webcam
video = cv2.VideoCapture(0)

# Encoding Image for Different People
samratEncoding = encodeDirectory("Samrat")
caitlinEncoding = encodeFace("People/caitlin.jpg")
vijayEncoding = encodeFace("People/vijay.jpg")
cassidyEncoding = encodeFace("People/cassidy.jpg")
nehaEncoding = encodeFace("People/neha.jpg")
ananthEncoding = encodeFace("People/ananth.jpg")
niharikaEncoding = encodeFace("People/niharika.jpg")
ananthramEncoding = encodeFace("People/ananthram.jpg")
ryanEncoding = encodeFace("People/ryan.jpg")
matthewEncoding = encodeFace("People/matthew.jpg")

# List For Face Encodings
faceEncodingsKnown = [
    samratEncoding,
    caitlinEncoding,
    vijayEncoding,
    cassidyEncoding,
    nehaEncoding,
    ananthEncoding,
    niharikaEncoding,
    ananthramEncoding,
    ryanEncoding,
    matthewEncoding
]

# List For Face Names
faceNamesKnown = [
    "Samrat",
    "Caitlin",
    "Vijay",
    "Cassidy",
    "Neha",
    "Ananth",
    "Niharika",
    "Ananthram",
    "Ryan",
    "Matthew"
]

faceLocations = []
faceEncodings = []
faceNames = []
processThisFrame = True
samratHere = True
caitlinHere = True
vijayHere = True
cassidyHere = True
nehaHere = True
ananthHere = True
niharikaHere = True
ananthramHere = True
ryanHere = True
matthewHere = True

file = open("AttendanceSheet.txt", "w")

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
        checkIfHere(name, 'Samrat')
        checkIfHere(name, 'Caitlin')
        checkIfHere(name, 'Vijay')
        checkIfHere(name, 'Cassidy')
        checkIfHere(name, 'Neha')
        checkIfHere(name, 'Ananth')
        checkIfHere(name, 'Niharika')
        checkIfHere(name, 'Ananthram')
        checkIfHere(name, 'Ryan')
        checkIfHere(name, 'Matthew')

    # Show Frame
    cv2.imshow('frame', frame)

    # If q is pressed, exit loop
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

# Upon exiting while loop, close web cam
video.release()
