EncodingModel.py
================
The ``EncodingModel.py`` File serves as the core for the encoding process. This allows images to be converted into usable data for the computer to use.

Imports
-------

.. code-block:: python

    import face_recognition
    import numpy as np
    import os
    from init import faceNamesKnown, faceEncodingsKnown, encodingNames

Methods
-------
The ``encodeFace()`` method takes in an image path and return an encoding after having analyzed the image.

.. code-block:: python

    def encodeFace(imageDirectory):
        # Load Images
        image = face_recognition.load_image_file(imageDirectory)
        # Encode Images
        encoding = face_recognition.face_encodings(image, None, 5)[0]
        return encoding

The ``encodeDirectory()`` method takes in a directory of images and returns an average encoding after having analyzed the multiple images. It takes advantage of the ``encodeFace()``
method to encode several images. It then adds up the encodings and takes the average of all of the encodings.

.. code-block:: python

    # Method encodes a directory of images and returns the average encoding of the images
    def encodeDirectory(directoryName):
        # Create list for all encodings
        allEncodings = []
        # Go through directory of files
        for filename in os.listdir("People Images/" + directoryName):
            # Get amount of files in directory
            fileAmount = len(next(os.walk("People Images/" + directoryName)))
            if filename.endswith(".jpg"):
                # iterate through files in directory
                for fileNum in range(0, fileAmount - 1):
                    # Add encodings to list
                    allEncodings.append(encodeFace("People Images/" + directoryName + "/" + str(fileNum) + ".jpg"))
        # List Length
        listLength = len(allEncodings)
        # Return average of encoded arrays array
        return sum(allEncodings) / listLength

Main Method
-----------
The main method will encode every directory in the ``People Images`` folder and save the files for each respective person in the ``Encodings`` folder.

.. code-block:: python

    for x in range(0, len(faceNamesKnown)):
        faceEncodingsKnown[x] = encodeDirectory(faceNamesKnown[x])
        np.save('Encodings/' + encodingNames[x], faceEncodingsKnown[x])