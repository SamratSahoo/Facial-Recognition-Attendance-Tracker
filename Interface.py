import sys
from flask import render_template, Flask, Response
from webui import WebUI
from Camera import VideoCamera
import os
from shutil import copyfile
from DynamicAddition import dynamicAdd
from Excel import markAbsentUnmarkedExcel

app = Flask(__name__)
ui = WebUI(app, debug=True)

global cameraState, addState, frames, framesRaw, onlineState
cameraState = False
addState = False
onlineState = False
framesRaw = []
frames = []


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
        finalPath = os.path.join(os.path.expanduser("~"), "Downloads/AttendanceExcel.xls")
        copyfile('AttendanceExcel.xls', finalPath)
    except Exception as e:
        print(e)

    return render_template('index.html')


@app.route('/start-camera')
def startCamera():
    global cameraState
    cameraState = True
    return render_template('index.html')


@app.route('/stop-camera')
def stopCamera():
    global cameraState
    cameraState = False
    markAbsentUnmarkedExcel()
    return render_template('index.html')


def gen(camera):
    global addState, cameraState, frames, framesRaw, onlineState
    while cameraState or addState:
        if not addState:
            global frames, framesRaw
            frame = camera.getFrame()
            frames.append(frame)
            framesRaw.append(camera.getRawFrame())
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        if addState:
            frameToSave = len(frames) - 1
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frames[frameToSave] + b'\r\n\r\n')
            try:
                dynamicAdd((framesRaw[frameToSave]))
                camera.additionProcess()
                cameraState = True
                addState = False
            except Exception as e:
                exceptionType, exceptionObject, exceptionThrowback = sys.exc_info()
                fileName = os.path.split(exceptionThrowback.tb_frame.f_code.co_filename)[1]
                print(exceptionType, fileName, exceptionThrowback.tb_lineno)
                print(e)
            break

        if onlineState:
            camera.goOnline()
            onlineState = False

    markAbsentUnmarkedExcel()


@app.route('/add-face')
def addFace():
    global addState
    addState = True
    return render_template('index.html')


@app.route('/online-mode')
def onlineMode():
    global onlineState
    onlineState = True
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera(source=-1)),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    try:
        ui.run()
    except Exception as e:
        print(e)
