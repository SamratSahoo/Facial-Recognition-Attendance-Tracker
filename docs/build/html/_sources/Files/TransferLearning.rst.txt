TransferLearning.py
===================
The TransferLearning.py file has been abandoned. However, many methods within ``TransferLearning.py`` are used in other modules. ``TransferLearning.py`` used to be the original core file until the switch to ``Interface.py``.

Imports
-------

.. code-block:: python

    import sys
    from init import *
    from Sheets import *
    from DynamicAddition import *
    import cv2
    import face_recognition
    import numpy as np
    import os
    from multiprocessing import Process
    from LivenessDetection import getModel

* ``os``: Necessary to access file systems
* ``sys``: Necessary to access the operating system
* ``cv2``: Necessary to access computer vision tools
* ``face_recognition``: Necessary to access face recognition tools
* ``init``: Necessary to access the arrays
* ``numpy``: Necessary to access Linear Algebra functions
* ``LivenessDetection``: Necessary to access the Liveness Detection models
* ``Sheets``: Necessary to access Google Sheets methods
* ``DynamicAddition``: Necessary to access DynamicAddition method
* ``multiprocessing``: Necessary to run multiple methods at once

Variables
---------
``TransferLearning.py`` takes advantage of global variables in order to modularize the complete file. Below are all the global variables in ``TransferLearning.py``.

.. code-block:: python

    global fullStudentNames, faceNamesKnown, encodingNames, model, video, encodingList, faceLocations, faceEncodingsKnown
    global faceEncodings, faceNames, inputFrames, processThisFrame, x, file, smallFrame, rgbFrame, livenessVal, name

Methods
-------
The ``checkIfHere()`` method makes sure that each name found in the frame only appears once.

.. code-block:: python

    def checkIfHere(name, nameToCheck):
        if name is nameToCheck:
            with open("AttendanceSheet.txt", 'r') as f:
                if nameToCheck in f.read():
                    pass
                else:
                    with open("AttendanceSheet.txt", 'a') as f2:
                        f2.write(name + "\n")
                        f2.close()

The ``getFolderSize()`` method returns the folder size of a given folder.

.. code-block:: python

    # Method to get amount of files in a certain folder
    def getFolderSize(folderName):
        fileList = os.listdir(folderName)
        numberFiles = len(fileList)
        return numberFiles

The ``adjustBrightness()`` method takes advantage of HSV values in order to adjust the brightness when the frame is too dark.

.. code-block:: python

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

The ``toList()`` method, ``loadLists()``, and ``loadDictionary()`` methods are used in order to manipulate the text files in ``List Information/`` and load all the arrays with the
correct information.

.. code-block:: python

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

The ``runInParallel()`` method allows us to run function in parallel. It is most notably used for dynamic addition.

.. code-block:: python

    def runInParallel(*fns):
        proc = []
        for fn in fns:
            p = Process(target=fn)
            p.start()
            proc.append(p)
        for p in proc:
            p.join()

The ``getLivenessValue()`` method manipulates the matrices of the last 24 frames and is able to return a liveness value from 0 to 1. The higher the value the more live the
frame is.

.. code-block:: python

    def getLivenessValue(frame, inputFrames, model):
        livenessFrame = cv2.resize(frame, (100, 100))
        livenessFrame = cv2.cvtColor(livenessFrame, cv2.COLOR_BGR2GRAY)
        inputFrames.append(livenessFrame)
        input = np.array([inputFrames[-24:]])
        input = input / 255
        if input.size == 240000:
            input = input.reshape(1, 24, 100, 100, 1)
            pred = model.predict(input)
            return pred[0][0]
        return 0.96

Omitted Method Documentation
-----------------------------
Due to similarities in ``TransferLearning.py`` and ``Camera.py``, documentation for the ``preProcess()``, ``optimizeWebcam()``, ``recognizeFaces()``, ``dynamicallyAdd()``,
``writeOnStream()``, and ``writeToFile()`` methods have been omitted in this page and have instead have their documentations on the ``Camera.py`` documentation. This allows
for the brevity of documentation.

Main Method
-----------
The main method here combines several of the methods in order to to put together the complete application. When ``q`` is pressed, the application will end.

.. code-block:: python

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

    markAbsentUnmarked()
