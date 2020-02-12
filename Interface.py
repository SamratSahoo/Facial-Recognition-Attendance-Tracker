from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture

import cv2


class CamApp(App):

    def build(self):
        self.img1 = Image()
        layout = BoxLayout()
        layout.add_widget(self.img1)
        layout.add_widget(Button(text='Hello World'))

        # Open CV Capture
        self.capture = cv2.VideoCapture(0)
        cv2.namedWindow("CV2 Image")
        Clock.schedule_interval(self.update, 1.0 / 33.0)
        return layout

    def update(self, dt):
        # Read OpenCV Camera
        ret, frame = self.capture.read()
        # Show OpenCV
        cv2.imshow("CV2 Image", frame)

        # Convert Open CV to Kivy Texture
        buf1 = cv2.flip(frame, 0)
        buf = buf1.tostring()
        texture1 = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
        texture1.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')

        # display image from the texture
        self.img1.texture = texture1


if __name__ == '__main__':
    CamApp().run()
    cv2.destroyAllWindows()
