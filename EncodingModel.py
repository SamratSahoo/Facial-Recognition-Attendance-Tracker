import face_recognition
import numpy as np
import os
from init import faceNamesKnown, faceEncodingsKnown, encodingNames


# Loads & Encode Images
def encodeFace(imageDirectory):
    # Load Images
    image = face_recognition.load_image_file(imageDirectory)
    # Encode Images
    encoding = face_recognition.face_encodings(image, None, 5)[0]
    return encoding


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


# Encode Directories for people + Save Encodings
for x in range(0, len(faceNamesKnown)):
    faceEncodingsKnown[x] = encodeDirectory(faceNamesKnown[x])
    np.save('Encodings/' + encodingNames[x], faceEncodingsKnown[x])
