Camera.py
==============
The ``Camera.py`` file serves to be the connection between the HTML dashboard and the OpenCV camera. The Camera.py file controls
all the camera functions.

Imports
-------

.. code-block:: python

   import os
   import sys
   import cv2
   import face_recognition
   from TransferLearning import loadDictionary, loadLists, toList, getLivenessValue, runInParallel, dynamicAdd, \
       getFolderSize, checkIfHere
   from init import *
   import numpy as np
   from Excel import *
   from LivenessDetection import getModel, getModelPred
   import socket
   from Sheets import *
   from timeit import default_timer as timer

* ``os``: Necessary to access file systems
* ``sys``: Necessary to access the operating system
* ``cv2``: Necessary to access computer vision tools
* ``face_recognition``: Necessary to access face recognition tools
* ``TransferLearning``: Necessary to access helper methods in original program
* ``init``: Necessary to access the arrays
* ``numpy``: Necessary to access Linear Algebra functions
* ``Excel``: Necessary to access Microsoft Excel methods
* ``LivenessDetection``: Necessary to access the Liveness Detection models
* ``socket``: Necessary to check internet connection
* ``Sheets``: Necessary to access Google Sheets methods
* ``timeit``: Necessary to take times

Feature Control Variables
-------------------------
These variables serve to control different features related to the camera

.. code-block:: python

   global dynamicState
   global pauseState
   global onlineMode
   dynamicState = False
   pauseState = True
   onlineMode = False

* ``dynamicState``: Controls whether you want to add a new person or not
* ``pauseState``: Controls whether the camera will be paused or not
* ``onlineState``: Controls whether to use google sheets or excel

Static Functions
----------------
The ``addPerson()`` toggles the ``dynamicState`` variable from True to False and vice versa.

.. code-block:: python

   def addPerson():
    global dynamicState
    dynamicState = True

The ``internetCheck()`` function will use the socket class and try to create a connection with Google.com. If it fails, it will throw an Exception and return False.

.. code-block:: python

   def internetCheck():
    try:
        socket.create_connection(("www.google.com", 80))
        return True
    except OSError:
        pass
    return False

Objects
--------
The VideoCamera Object initializes with several starting variable amounts including initial arrays, liveness models, timestamps, encodings, and internet connections.

.. code-block:: python

       def __init__(self, source):
        try:
            # Call on OpenCV Video Capture
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

When it is destroyed, it deletes the camera.

.. code-block:: python

    def __del__(self):
        # Delete Video Capture
        self.video.release()

Object Functions
----------------

The ``addFace()`` function will apply the ``dynamicAdd()`` from ``TransferLearning.py`` if and only if a face is found and it is Unknown. It will then reload all of the arrays and encodings, At the end, it will turn the ``dynamicState`` variable to False.

.. code-block:: python

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

The ``getRawFrame()`` function will return solely the frame the OpenCV camera sees.

.. code-block:: python

    def getRawFrame(self):
        # Returns the raw frame
        _, frameToReturn = self.video.read()
        return frameToReturn

The ``goOnline()`` function will control the onlineMode feature control variable to control whether to use online or offline mode.

.. code-block:: python

    def goOnline(self):
        global onlineMode
        onlineMode = not onlineMode

The ``getFrame()`` function is the core function and has been split into different parts for the purpose of readability and easier to understand documentation.

Here we are declaring some global variables that are used universally throughout ``Camera.py``

.. code-block:: python

    def getFrame(self):
        try:
            # Some global variables
            global processThisFrame, faceLocations, faceNames, encodingList, faceNamesKnown, fullStudentNames
            global model, inputFrames, frame, dynamicState, start, internetCheck, onlineMode

Next we are reading the frame and converting it into the correct dimensions and formats for our needs. This also includes calculating the elapsed time.

.. code-block:: python

        # Read OpenCV video
        success, frame = self.video.read()
        # Resize as necessary
        smallFrame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        # Change Colors as necessary
        rgbSmallFrame = smallFrame[:, :, ::-1]
        # End time for Late feature
        end = timer()
        # Calculate time spent
        elapsedTime = end - start

We are then using the ``processThisFrame`` variable to process every other frame so that the User Experience is better. We also calcualte the locations and encodings of the faces
in the current frame being analyzed. We declared an empty list that will store all face names in the frame.

.. code-block:: python

        # Only process every other frame of video to save time
        if processThisFrame:
            # Find all the faces and face encodings in the current frame of video
            faceLocations = face_recognition.face_locations(rgbSmallFrame)
            faceEncodings = face_recognition.face_encodings(rgbSmallFrame, faceLocations)

            # Empty Face names for every iteration
            faceNames = []

We then calculate the blur amount using a Laplacian function and if the blur is low enough we will perform face recognition to the frame. The face recognition is done
through calculating a Frobenius Norm to find the variance between saved encodings and encodings within the frame. The lowest variance is the face that is recognized. If the variance
is an outlier, then it will assume the face is not in the database and give it an unknown tag.

.. code-block:: python

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

This will calculate the coordinates to draw the faces. It also calculates liveness values and blur amounts once again.

.. code-block:: python

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

This part will actually draw the box with a name if and only if the image is alive.

.. code-block:: python

                # if liveness is over 95% then continue recognition
                if livenessVal > 0.95:
                    # Blur must be over 40 in order to accurately recognize a face
                    if blurAmount > 40:
                        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

This part will check if the User is online or offline and their respective mode. If they are online and in online mode, it will record attendance on Google Sheets.
This part will also check if they are late or not.

.. code-block:: python

                # Online/Offline Mode
                        if internetCheck and onlineMode:
                            for x in range(0, len(fullStudentNames)):
                                if name in fullStudentNames[x]:
                                    # Check if they are late
                                    if elapsedTime > 300:
                                        updateLatePerson()
                                    else:
                                        updatePresentPerson()

If they are offline it will put it on the Microsoft Excel sheet.

.. code-block:: python

                        else:
                            for x in range(0, len(fullStudentNames)):
                                if name in fullStudentNames[x]:
                                    # Check if they are late
                                    if elapsedTime > 300:
                                        updateLatePersonExcel(fullStudentNames[x])
                                    else:
                                        updatePresentPersonExcel(fullStudentNames[x])

This will record it on the text file

.. code-block:: python

                        for x in range(0, len(faceNamesKnown)):
                            checkIfHere(name, faceNamesKnown[x])

If it is a spoof, it will warn the user,

.. code-block:: python

                else:
                    # Do not mark anyone if its a spoof
                    cv2.putText(frame, "WARNING: SPOOF DETECTED", (100, 75), font, 1.0, (0, 0, 255), 2)

This will encode the frame into a .jpeg file so that it can be displayed on the Flask Dashboard.

.. code-block:: python

            # Encode frame so it can be displayed on a webpage
            ret, jpeg = cv2.imencode('.jpg', frame)
            return jpeg.tobytes()

This will catch any potential errors that may occur.

.. code-block:: python

        except Exception as e:
            # Enceptions to get file + line numbers errors are on
            exceptionType, exceptionObject, exceptionThrowback = sys.exc_info()
            fileName = os.path.split(exceptionThrowback.tb_frame.f_code.co_filename)[1]
            print(exceptionType, fileName, exceptionThrowback.tb_lineno)
            print(e)