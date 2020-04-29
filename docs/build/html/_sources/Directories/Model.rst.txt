Model
===============
The Model directory holds the machine learning models that are used for liveness detection. Within the directory there are 2 files:
the H5 model file and the Json model file.

   * ``model.h5``: This file holds the actual distribution of data for the model. It is then run through Keras using the ``LivenessModel.py`` to process this data into usable information
   * ``model.json``: This is a file that also holds model information with the necessary requirements to process the model. This file is actually readable to humans.