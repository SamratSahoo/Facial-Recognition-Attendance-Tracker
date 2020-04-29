import os
from init import faceNamesKnown, faceEncodingsKnown, encodingNames
from Sheets import *


def getFolderSize():
    folderSize = len(next(os.walk("People Images/" + str(faceNamesKnown[x])))) - 1
    if folderSize < 2:
        folderSize = 2
    return folderSize


if __name__ == '__main__':
    for x in range(0, len(faceNamesKnown)):
        if getFolderSize() == 2:
            formatPage()
            import TransferLearning
