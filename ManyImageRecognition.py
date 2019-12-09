# THIS FILE IS IN PROGRESS
import cv2

video = cv2.VideoCapture(0)

while True:
    try:
        ret, frame = video.read()
    except Exception as e:
        print(e)
