# ISM-Original-Work
### Program Preface
 This project was made for the Independent Study 
 Mentorship Program. The Independent Study Mentorship 
 Program is a rigorous research-based program offered 
 at Frisco ISD schools for passionate high-achieving 
 individuals.

Throughout the course of the program, students 
carry-out a year-long research study where they 
analyze articles and interview local professionals. 
Through the culmination of the research attained, 
students create an original work, presented at 
research showcase, and a final product that will be 
showcased at final presentation night. Through the 
merits of this program, individuals are able to follow 
their passions while increasing their prominence in the 
professional world and growing as a person.

The ISM program is a program in which students carry-on skills that not only last for the year, but for life. ISM gives an early and in-depth introduction to the students' respective career fields and professional world. Coming out of this program, students are better equipped to handle the reality of the professional world while having become significantly more knowledgeable of their respective passions. The ISM program serves as the foundation for the success of individuals in the professional world.
### Project Preface 
 Facial Recognition Based Attendance Tracker: This 
 attendance system uses image datasets to create an
 average encoding of the person. This encoding is 
 then compared with frame encodings from the camera 
 stream. Down below is the documentation for each 
 part of this application
 
### Documentation
* `Cascades `
 This is the folder that contains OpenCV haar cascades to 
be for facial detection. It was being used, however, after 
switch to the facial_recognition class it is no longer used.
It may be used in the future.
* `Encodings` 
This is where all the encodings for the processed images in EncodingsModel.py
are saved. They are saved as numpy files which are later loaded into TransferLearning.py.
* `Example Executions` 
This is where the example pictures of Application.py executions can be found. In this folder,
you can find the actual face recognition occurring through the webcam.
* `People`
This folder contains several more directories for the people 
to be detected and recognized in the application. Within the 
subdirectories, there the images which are analyzed and converted 
into an array and compared with the video stream.
* `Application.py`
This is the application that will be executed to run the main body of the program
* `AttendanceSheet.txt`
This is a text file where the names of the people detected are outputted. This will 
likely be replaced in the future with a connection to the Google Sheets API.
* `EncodingModel.py`
This is where all the encodings are done. When this python file is run,
it will encode the images in the saved directory and save the returned encodings
into numpy file found in the Encodings folder.
* `init.py`
This file is used to access all the encoding and name variables that are used universally
throughout the application
* `Interface.py`
This file is where the graphical user interface for the attendance tracker can be found. It was developed
using the Kivy python library
* `Sheets.py`
This file is where all the Google Sheets API formatting can be found. Please note for this you will need to obtain your
own Google Sheets and Google Drive credentials through Google Cloud.
* `TransferLearning.py`
This is where facial recognition with small amounts of data is done. It uses one-shot learning by converting encodings
from datas ets in the People folder. It compares these encodings to the encodings in the webcam and whichever encoding
is the most similar, it outputs that name. 
Further documentation can be found within
the program comments.

### Requirements
You will need Python 3.6 and the following libraries installed:
* dlib
* face_recognition 
* opencv-python
* opencv-contrib-python
* numpy
* kivy
* pygsheets
* gspread-formatting
* oauth2client

### Portfolio
My research and work for this year can be found at my
[Digital Portfolio](https://samratsahoo.weebly.com)

### Thank You
I would just like to give a  special thank you to [Adam Geitgey](https://github.com/ageitgey) for 
the creation of his facial_recognition class. 

I would also like to give a special thanks to the following individuals for their contributions
to my research throughout this project.
* Trey Blankenship [Raytheon]
* Won Hwa Kim [UT Arlington]
* Tim Cogan [ams AG]
* Vijay Nidumolu [Samsung Electronics America]
* Sehul Viras [Dallas Baptist University & IntelliCentric]

One last thank you for the [Radicubs Robotics Team](https://radicubs.wixsite.com/robotics) for 
helping me test this attendance tracker. 
