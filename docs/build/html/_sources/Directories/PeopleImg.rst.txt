People Images Folder
====================
The People images folder is the local database of photos for each person. Within the People Images folder you will see subdirectories
of each of the names found in ``List Information/Face Names Known`` and each subdirectory holds the respective photos of that person. Within
each person subdirectory you will see 2 photos, ``0.jpg, 1.jpg``

JPG File Names Explained
------------------------
The JPG files are named ``0.jpg, 1.jpg`` respectively because within ``EncodingModel.py`` we have a method called ``encodeDirectory()``
which requires at least 2 images to process and outputs an embeeding to ``Encodings/``. The ``0.jpg, 1.jpg`` are the two files that it processes.