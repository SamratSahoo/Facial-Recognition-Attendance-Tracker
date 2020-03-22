from flask import render_template, Flask
import cv2
from webui import WebUI
import os
from shutil import copyfile
import faulthandler

app = Flask(__name__)
ui = WebUI(app, debug=True)
global video, cameraState
cameraState = True
video = cv2.VideoCapture(0)


@app.route('/')
@app.route('/index')
def indexPage():
    return render_template('index.html')


@app.route('/configure')
def configurePage():
    return render_template('configurations.html')


@app.route('/attendance')
def attendancePage():
    return render_template('attendance.html')


@app.route('/settings')
def settingsPage():
    return render_template('settings.html')


@app.route('/contact')
def contactPage():
    return render_template('contact.html')


@app.route('/help')
def helpPage():
    return render_template('help.html')


@app.route('/start-camera')
def startCamera():
    # while cameraState:
    #     _, frame = video.read()
    #     cv2.imshow("yes", frame)
    return render_template('index.html')

@app.route('/download-text')
def downloadText():
    try:
        finalPath = os.path.join(os.path.expanduser("~"), "Downloads/AttendanceSheet.txt")
        copyfile('AttendanceSheet.txt', finalPath)
    except Exception as e:
        print(e)
    return render_template('index.html')


@app.route('/download-excel')
def downloadExcel():
    try:
        finalPath = os.path.join(os.path.expanduser("~"), "Downloads/AttendanceExcel.xlsx")
        copyfile('AttendanceExcel.xlsx', finalPath)
    except Exception as e:
        print(e)

    return render_template('index.html')


if __name__ == '__main__':
    try:
        ui.run()
    except Exception as e:
        print(e)
