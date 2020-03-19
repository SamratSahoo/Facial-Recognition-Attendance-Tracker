from flask import render_template, Flask
import cv2
from webui import WebUI

app = Flask(__name__)
ui = WebUI(app, debug=True)


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


@app.route('/json')
def json():
    return render_template('json.html')

@app.route('/contact')
def contactPage():
    return render_template('contact.html')

@app.route('/hello')
def hello():
    print("meow")
    return render_template('configurations.html')


# @app.route('/background_process_test')
# def background_process_test():
#     video = cv2.VideoCapture(0)
#     while True:
#         ret, frame = video.read()
#         cv2.imshow('Frame', frame)
#     return ("nothing")


if __name__ == '__main__':
    try:
        ui.run()
    except Exception as e:
        print(e)
