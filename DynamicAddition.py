import cv2
import os
from EncodingModel import *
import numpy as np



def pauseCamera():
    cv2.waitKey(-100)


def dynamicAdd(image):
    firstName = input("What is your first name: ")
    lastName = input("What is your last name: ")
    fullName = firstName + " " + lastName
    with open("List Information/Full Student Names", "a") as f:
        f.write(fullName)
        f.write("\n")
        f.close()

    with open("List Information/Face Names Known", "a") as f:
        f.write(firstName)
        f.write("\n")
        f.close()
    with open("List Information/Encoding Names", "a") as f:
        f.write(firstName + "Encoding.npy")
        f.write("\n")
        f.close()

    os.makedirs("People Images/" + firstName)
    cv2.imwrite(os.path.join("People Images/" + firstName, '0.jpg'), image)
    cv2.imwrite(os.path.join("People Images/" + firstName, '1.jpg'), image)

    print(firstName)
    encoding = encodeDirectory(firstName)
    np.save('Encodings/' + str(firstName).replace(" ", "") + 'Encoding.npy', encoding)
