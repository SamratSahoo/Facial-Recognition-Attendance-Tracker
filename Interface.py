from flask import Flask, escape, request, render_template, Response
import cv2

app = Flask(__name__)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def startApplication():
    return render_template('dashboard.html')


@app.route('/exec')
def hello():
    while True:
        print("Meow")
    return ("None")


if __name__ == '__main__':
    app.run(debug=True)
