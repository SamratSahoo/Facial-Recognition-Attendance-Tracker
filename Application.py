import os
from init import faceNamesKnown, faceEncodingsKnown, encodingNames


def getFolderSize():
    folderSize = len(next(os.walk("People/" + str(faceNamesKnown[x])))) - 1
    if folderSize < 2:
        folderSize = 2
    return folderSize


for x in range(0, len(faceNamesKnown)):
    if getFolderSize() == 2:
        import FewImageRecognition

        continue
    else:
        for x in range(0, len(faceNamesKnown)):
            if getFolderSize() > 2:
                import ManyImageRecognition
