LivenessDetection.py
====================
The ``LivenessDetection.py`` file controls the LivenessDetection model processing which differentiates real faces from flat images.

Imports
-------

.. code-block:: python

    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import Dense, Dropout, Flatten
    from tensorflow.keras.layers import Conv3D, MaxPooling3D

* ``Keras``: Necessary for deep learning functions to process the model

Methods
-------
The ``getModel()`` method is used to process the data within a model so that is more usable. This is done through a Sequential model with several layers to correctly process the data.

.. code-block:: python

    def getModel():
        model = Sequential()
        model.add(Conv3D(32, kernel_size=(3, 3, 3),
                         activation='relu',
                         input_shape=(24, 100, 100, 1)))
        model.add(Conv3D(64, (3, 3, 3), activation='relu'))
        model.add(MaxPooling3D(pool_size=(2, 2, 2)))
        model.add(Conv3D(64, (3, 3, 3), activation='relu'))
        model.add(MaxPooling3D(pool_size=(2, 2, 2)))
        model.add(Conv3D(64, (3, 3, 3), activation='relu'))
        model.add(MaxPooling3D(pool_size=(2, 2, 2)))
        model.add(Dropout(0.25))
        model.add(Flatten())
        model.add(Dense(128, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(2, activation='softmax'))

        return model

The ``getModelPred()`` method is used to simply initialize and load the model with its respective weights.

.. code-block:: python

    def getModelPred():
        model = getModel()
        model.load_weights("Model/model.h5")
        return model