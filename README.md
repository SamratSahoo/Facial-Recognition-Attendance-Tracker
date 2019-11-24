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
 stream Down below is the documentation for each 
 part of this application
 
### Documentation
* `Cascades `
 This is the folder that contains OpenCV haar cascades to 
be for facial detection. It was being used, however, after 
switch to the facial_recognition class it is no longer used.
It may be used in the future.
* `Encodings` 
This is where all the encodings for the processed images in EncodingsModel.py
are saved. They are saved as numpy files which are later loaded into Application.py.
* `People`
This folder contains several more directories for the people 
to be detected and recognized in the application. Within the 
subdirectories, there the images which are analyzed and converted 
into an array and compared with the video stream.
* `Application.py`
This is the body of the application where the image processing
and video analysis occurs. Running this file will open up
a video stream where the you will be able to see a blue box with the person's
name under the box drawn. Further documentation can be found within
the program comments.
* `AttendanceSheet.txt`
This is a text file that is where the names of the people detected
are outputted. This will likely be replaced in the future
with a connection to the Google Sheets API.
* `EncodingModel.py`
This is where all the encodings are done. When this python file is run,
it will encode the images in the saved directory and save the returned encodings
into numpy file found in the Encodings folder.

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

One last thank you for the Radicubs Robotics Team for 
helping me test this attendance tracker. 
