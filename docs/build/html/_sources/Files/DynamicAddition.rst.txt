DynamicAddition.py
==================
The ``DynamicAddition.py`` file serves as a file that houses helper methods to assist with the dynamic addition process.

Imports
-------

.. code-block:: python

    import cv2
    from EncodingModel import *
    import numpy as np

* ``cv2``: Necessary to access computer vision tools
* ``EncodingModel``: Necessary to access modules to encode images into usable data
* ``numpy``: Necessary to access Linear Algebra functions

Methods
-------
The ``pauseCamera()`` method is used to pause the camera. This is no longer used but was once used in ``TransferLearning.py``

.. code-block:: python

    def pauseCamera():
        cv2.waitKey(-100)

The ``dynaicAdd()`` method is used to add faces. This method was also once used in ``TransferLearning.py`` but since has been abandoned.
This gets the full name of the person.

.. code-block:: python

    def dynamicAdd(image):
        firstName = input("What is your first name: ")
        lastName = input("What is your last name: ")
        fullName = firstName + " " + lastName

Then the text files that store names of people are edited.

.. code-block:: python

    with open("List Information/Full Student Names", "a") as f:
        f.write(fullName)
        f.write("\n")
        f.close()

    with open("List Information/Face Names Known", "a") as f:
        f.write(firstName)
        f.write("\n")
        f.close()
    with open("List Information/Encoding Names", "a") as f:
        f.write(firstName + "Encoding.npy")
        f.write("\n")
        f.close()

Separate directories are made for each person to store their images and their images are saved

.. code-block:: python

    os.makedirs("People Images/" + firstName)
    cv2.imwrite(os.path.join("People Images/" + firstName, '0.jpg'), image)
    cv2.imwrite(os.path.join("People Images/" + firstName, '1.jpg'), image)

Their images are encoded and the encoding is saved as a numpy file.

.. code-block:: python

    encoding = encodeDirectory(firstName)
    np.save('Encodings/' + str(firstName).replace(" ", "") + 'Encoding.npy', encoding)

