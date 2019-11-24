import face_recognition
import numpy as np
import os

# Loads & Encode Images
def encodeFace(imageDirectory):
    # Load Images
    image = face_recognition.load_image_file(imageDirectory)
    # Encode Images
    encoding = face_recognition.face_encodings(image)[0]
    return encoding


# Method encodes a directory of images and returns the average encoding of the images
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

# Encode Directories for people
samratEncoding = encodeDirectory("Samrat")
caitlinEncoding = encodeDirectory("Caitlin")
vijayEncoding = encodeDirectory("Vijay")
cassidyEncoding = encodeDirectory("Cassidy")
nehaEncoding = encodeDirectory("Neha")
ananthEncoding = encodeDirectory("Ananth")
niharikaEncoding = encodeDirectory("Niharika")
ryanEncoding = encodeDirectory("Ryan")
matthewEncoding = encodeDirectory("Matthew")
shrenikEncoding = encodeDirectory("Shrenik")

# Save Encodings into Numpy file
np.save('Encodings/SamratEncoding', samratEncoding)
np.save('Encodings/CaitlinEncoding', caitlinEncoding)
np.save('Encodings/VijayEncoding', vijayEncoding)
np.save('Encodings/CassidyEncoding', cassidyEncoding)
np.save('Encodings/NehaEncoding', nehaEncoding)
np.save('Encodings/AnanthEncoding', ananthEncoding)
np.save('Encodings/NiharikaEncoding', niharikaEncoding)
np.save('Encodings/RyanEncoding', ryanEncoding)
np.save('Encodings/MatthewEncoding', matthewEncoding)
np.save('Encodings/ShrenikEncoding', shrenikEncoding)