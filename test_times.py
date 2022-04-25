import cv2

import Drone
import time


def test_computer_drone_computer(drone):
    total = 0
    number_of_iter = 50
    for i in range(number_of_iter):
        im = drone.getFrame()
        t1 = time.time()
        blob = cv2.dnn.blobFromImage(im, 1 / 255.0, (416, 416), swapRB=True, crop=False)
        drone.detector.net.setInput(blob)
        person = drone.detector.net.forward(drone.detector.ln)
        t2 = time.time()
        total += t2 - t1

    return total / number_of_iter


if __name__ == '__main__':
    myDrone = Drone.Drone()
    print(test_computer_drone_computer(myDrone))
