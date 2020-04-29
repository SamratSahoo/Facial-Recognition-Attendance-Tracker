Application.py
==============
The Application.py file was originally used to run the core application by checking if there were enough images in each of the respective folders in ``People Images``
but now has been abandoned.

Imports
-------
.. code-block:: python

   import os
   from init import *
   from Sheets import *

* os: Necessary to access file systems
* init: Necessary to access the arrays
* Sheets: Necessary to access the formatPage() method that is later used

Functions
----------
The ``getFolderSize()`` function makes sure there are at least 2 images in each subdirectory in the ``PeopleImages/`` directory before proceeding with the application.

.. code-block:: python

   def getFolderSize():
    folderSize = len(next(os.walk("People/" + str(faceNamesKnown[x])))) - 1
    if folderSize < 2:
        folderSize = 2
    return folderSize

Main Method
-----------
The main method will run ``TransferLearning.py`` if all of the folders have the correct amount of images.

.. code-block:: python

   if __name__ == '__main__':
    for x in range(0, len(faceNamesKnown)):
        if getFolderSize() == 2:
            formatPage()
            import TransferLearning