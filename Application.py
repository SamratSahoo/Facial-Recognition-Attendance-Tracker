import os
from init import *
# from Sheets import *


def getFolderSize():
    folderSize = len(next(os.walk("People Images/" + str(faceNamesKnown[x])))) - 1
    if folderSize < 2:
        folderSize = 2
    return folderSize


for x in range(0, len(faceNamesKnown)):
    formatPage()
    if getFolderSize() == 2:
        pass
