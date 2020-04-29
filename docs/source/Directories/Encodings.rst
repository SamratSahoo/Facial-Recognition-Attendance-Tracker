Encodings
===============
In software development, taking into account the runtime is easily one of the most important aspects of developing a powerful
program. In this project, the Encodings directory serves as one of the key features to reduce runtime. The Encodings directory
houses several files such as ``SamratEncoding.npy``. This is a numpy file in what is known as an embedding.

Purpose in Facial Recognition Process
-------------------------------------
In the image pre-processing state, it is necessary to convert raw images to usable data for the computer.
In order to do that, we convert the images into numpy arrays using the Histogram of Oriented Gradients algorithm.
These files hold numpy arrays for the information of the person so that the computer would not have to recalculate these arrays
every time the program is run. This drastically reduced runtime from 10 minutes to to 10 seconds. This was a major improvement
from the original program design that had to recalculate data over and over again.
