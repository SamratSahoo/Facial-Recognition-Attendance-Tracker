init.py
==============
The ``init.py`` file serves as a file where every file in the project can access globally declared arrays. This allows for shared variables within files.
All variables are empty because they are inputted respective values in other files.

Dictionaries
------------
The ``faceEncodingsKnown`` dictionary is used to hold an encoding name as its key and the respective encoding as its value.

.. code-block:: python

    faceEncodingsKnown = {

    }

Lists
-----
The ``faceNamesKnown`` list holds the first names only from the ``Face Names Known.txt`` file.

.. code-block:: python

    faceNamesKnown = [

    ]

The ``fullStudentNames`` list holds the first and last names from the ``Full Student Names.txt`` file.

.. code-block:: python

    fullStudentNames = [

    ]

The ``encodingNames`` list holds the encoding namesfrom the ``Encoding Names.txt`` file.

.. code-block:: python

    encodingNames = [

    ]
