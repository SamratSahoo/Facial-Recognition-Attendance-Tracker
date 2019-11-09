import cv2

# Load Cascade Classifier
import numpy as np

faceCascade = cv2.CascadeClassifier('Cascades/data/haarcascade_frontalface_alt.xml')

# Create Webcam
video = cv2.VideoCapture(0)

while (True):
    # Open Webcam
    ret, frame = video.read()

    # Analyze Gray Scale and increase brightness
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = np.uint8(np.double(gray) + 5)

    # Use Haar Cascade to find face
    faces = faceCascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    # Save Face as PNG
    for(x,y,w,h) in faces:
        roiGray = gray[y:y+h, x:x+w]
        roiColor = frame[y:y+h, x:x+w]
        imgItem = "myImage.png"
        cv2.imwrite(imgItem, roiGray)

        # Conditions for Rectangle
        color = (255,0,0)
        stroke = 2
        endX = x + w
        endY = y + h

        # Draw Rectangle
        cv2.rectangle(frame, (x, y), (endX, endY), color, stroke)

    # Show Frame
    cv2.imshow('frame', frame)

    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

# Upon exiting while loop, close web cam
video.release()
video.destroyAllWindows()
