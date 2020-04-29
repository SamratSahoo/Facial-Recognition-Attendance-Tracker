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
