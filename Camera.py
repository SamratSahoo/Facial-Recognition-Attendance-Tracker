import os
import sys

import cv2
import face_recognition

from DynamicAddition import pauseCamera
from TransferLearning import loadDictionary, loadLists, toList, getLivenessValue, runInParallel, dynamicAdd, \
    getFolderSize, checkIfHere
from init import *
import numpy as np
from Excel import *
from LivenessDetection import getModel, getModelPred
import socket
# from Sheets import * # Uncomment to use online/offline mode
from timeit import default_timer as timer

# Global Variables
global dynamicState
global pauseState
dynamicState = False
pauseState = True


# Dynamic Addition Variable
def addPerson():
    global dynamicState
    dynamicState = True


# Check Internet Function
def internetCheck():
    try:
        # connect to the host -- tells us if the host is actually
        # reachable
        socket.create_connection(("www.google.com", 80))
        return True
    except OSError:
        pass
    return False


# To make a video camera Object
class VideoCamera(object):
    # initializations of a Videocamera
    def __init__(self, source):
        try:
            # Video capture
            self.video = cv2.VideoCapture(source)

            # Some global variables
            global processThisFrame, faceLocations, faceEncodings, faceNames, encodingList, encodingNames
            global faceNamesKnown, fullStudentNames, inputFrames, model, start, internetCheck

            # Initialize variables
            faceLocations = []
            faceEncodings = []
            faceNames = []
            inputFrames = []
            processThisFrame = True

            # Load List information
            fullStudentNames = loadLists("List Information/Full Student Names")  # List with full Student Names
            faceNamesKnown = loadLists("List Information/Face Names Known")  # List With Face Names
            encodingNames = loadLists("List Information/Encoding Names")  # List With encoding names
            loadDictionary("List Information/Face Names Known", faceEncodingsKnown)  # Dictionary with Encodings
            encodingList = toList(faceEncodingsKnown)
            # Load encodings
            for x in range(0, int(len(encodingList))):
                encodingList[x] = np.load("Encodings/" + str(encodingNames[x]))

            # Load Liveness Model
            model = getModelPred()

            # Start Late timer
            start = timer()

            # Internet Check
            internetCheck = internetCheck()

        except Exception as e:
            print(e)

    def __del__(self):
        # Delete Video Capture
        self.video.release()

    # Dynamic Addition After-Function
    def additionProcess(self):

        # Some global variables
        global encodingList, encodingNames, faceEncodingsKnown
        global faceNamesKnown, fullStudentNames

        # Load Lists Again
        fullStudentNames = loadLists(
            "List Information/Full Student Names")  # List with full Student Names
        faceNamesKnown = loadLists("List Information/Face Names Known")  # List With Face Names
        encodingNames = loadLists("List Information/Encoding Names")  # List With encoding names
        loadDictionary("List Information/Face Names Known",
                       faceEncodingsKnown)  # Dictionary with Encodings

        # Run Encoding Model if necessary
        if getFolderSize("Encodings/") != len(encodingNames):
            import EncodingModel

        # Reload Encodings
        encodingList = toList(faceEncodingsKnown)
        for x in range(0, int(len(encodingList))):
            encodingList[x] = np.load("Encodings/" + str(encodingNames[x]))

    # Dyanic Addition Core Function
    def addFace(self):

        # Some global variables
        global dynamicState, encodingNames, fullStudentNames, faceNamesKnown, encodingList, frame

        # Only run Dynamic Addition if a face is found and is unknown
        if 'Unknown' in faceNames and len(faceLocations) > 1:
            # Run dynamic core addition
            dynamicAdd(frame)

            # Relaod Lists
            fullStudentNames = loadLists("List Information/Full Student Names")  # List with full Student Names
            faceNamesKnown = loadLists("List Information/Face Names Known")  # List With Face Names
            encodingNames = loadLists("List Information/Encoding Names")  # List With encoding names
            loadDictionary("List Information/Face Names Known", faceEncodingsKnown)  # Dictionary with Encodings

            # Run Encoding Model as necessary
            if getFolderSize("Encodings/") != len(encodingNames):
                import EncodingModel

            # Reload Enecodings
            encodingList = toList(faceEncodingsKnown)
            for x in range(0, int(len(encodingList))):
                encodingList[x] = np.load("Encodings/" + str(encodingNames[x]))

            # Turn off dynamic addition once done
            dynamicState = False

    def getRawFrame(self):
        # Returns the raw frame
        _, frameToReturn = self.video.read()
        return frameToReturn

    def getFrame(self):
        try:
            # Some global variables
            global processThisFrame, faceLocations, faceNames, encodingList, faceNamesKnown, fullStudentNames
            global model, inputFrames, frame, dynamicState, start, internetCheck

            # Read OpenCV video
            success, frame = self.video.read()
            # Resize as necessary
            smallFrame = cv2.resize(frame, (0,0), fx=0.25, fy=0.25)
            # Change Colors as necessary
            rgbSmallFrame = smallFrame[:, :, ::-1]
            # End time for Late feature
            end = timer()
            # Calculate time spent
            elapsedTime = end - start

            # Only process every other frame of video to save time
            if processThisFrame:
                # Find all the faces and face encodings in the current frame of video
                faceLocations = face_recognition.face_locations(rgbSmallFrame)
                faceEncodings = face_recognition.face_encodings(rgbSmallFrame, faceLocations)

                # Empty Face names for every iteration
                faceNames = []

                # Calculate Blur; if its too blurry it won't do facial recognition
                blurAmount = cv2.Laplacian(frame, cv2.CV_64F).var()
                if blurAmount > 40:
                    for faceEncoding in faceEncodings:
                        # See if the face is a match for the known face(s)
                        matchesFound = face_recognition.compare_faces(encodingList, faceEncoding)
                        name = "Unknown"

                        # Or instead, use the known face with the smallest distance to the new face
                        faceDistances = face_recognition.face_distance(encodingList, faceEncoding)
                        matchIndex = np.argmin(faceDistances)
                        if matchesFound[matchIndex]:
                            name = faceNamesKnown[matchIndex]
                        # Add name to the faceNames array
                        faceNames.append(name)
            # Process every other frame
            processThisFrame = not processThisFrame

            # Display the results
            for (top, right, bottom, left), name in zip(faceLocations, faceNames):
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                # Draw a box around the face
                cv2.rectangle(frame, (left, top), (right, bottom), (255, 0, 0), 2)

                # Draw a label with a name below the face
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (255, 0, 0), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                # Recalculate blur
                blurAmount = cv2.Laplacian(frame, cv2.CV_64F).var()
                # Calculate liveness amount
                livenessVal = getLivenessValue(frame, inputFrames, model)

                # if liveness is over 95% then continue recognition
                if livenessVal > 0.95:
                    # Blur must be over 40 in order to accurately recognize a face
                    if blurAmount > 40:
                        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
                        # Online/Offline Mode
                        if internetCheck:
                            for x in range(0, len(fullStudentNames)):
                                if name in fullStudentNames[x]:
                                    # Check if they are late
                                    if elapsedTime > 300:
                                        updateLatePersonExcel(fullStudentNames[x])
                                        # updateLatePerson() # Uncomment to use online/offline mode (GSheets)
                                    else:
                                        updatePresentPersonExcel(fullStudentNames[x])
                                        # updatePresentPerson() # Uncomment to use online/offline mode (GSheets)
                        else:
                            for x in range(0, len(fullStudentNames)):
                                if name in fullStudentNames[x]:
                                    # Check if they are late
                                    if elapsedTime > 300:
                                        updateLatePersonExcel(fullStudentNames[x])
                                    else:
                                        updatePresentPersonExcel(fullStudentNames[x])

                        for x in range(0, len(faceNamesKnown)):
                            checkIfHere(name, faceNamesKnown[x])
                else:
                    # Do not mark anyone if its a spoof
                    cv2.putText(frame, "WARNING: SPOOF DETECTED", (100, 75), font, 1.0, (0, 0, 255), 2)

            # Encode frame so it can be displayed on a webpage
            ret, jpeg = cv2.imencode('.jpg', frame)
            return jpeg.tobytes()
        except Exception as e:
            # Enceptions to get file + line numbers errors are on
            exceptionType, exceptionObject, exceptionThrowback = sys.exc_info()
            fileName = os.path.split(exceptionThrowback.tb_frame.f_code.co_filename)[1]
            print(exceptionType, fileName, exceptionThrowback.tb_lineno)
            print(e)
