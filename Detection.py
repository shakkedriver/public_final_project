import cv2
import numpy as np


class ObjectsDetector:
    def __init__(self, config_file, weights_file):
        self.net = cv2.dnn.readNetFromDarknet(config_file, weights_file)
        self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
        self.ln = self.net.getLayerNames()
        self.ln = [self.ln[i - 1] for i in self.net.getUnconnectedOutLayers()]

    """
    finds the bonding box with the highest probability with a person inside it [x, y, w, h]
    """

    def detect(self, img, prob=.5):
        h, w = img.shape[:2]
        blob = cv2.dnn.blobFromImage(img, 1 / 255.0, (416, 416), swapRB=True, crop=False)
        self.net.setInput(blob)
        person = self.net.forward(self.ln)
        person = np.vstack(person)
        person = person[:, :6]
        person = person[np.where(person[:, 5] > prob)]
        if person.shape[0] != 0:
            person = person[np.argmax(person[:, 5])]
        person = person.reshape((-1, 6))
        person[:, 0:4] *= np.array([w, h, w, h])
        person[:, 0] -= person[:, 2] // 2
        person[:, 1] -= person[:, 3] // 2
        return person

    def find_center(self, img):
        """
        [x,y,w,h,cx,cy,area]
        """
        person = self.detect(img)
        if person.shape[0] != 0:
            x = person[0][0]
            y = person[0][1]
            w = person[0][2]
            h = person[0][3]
            return [x, y, w, h, (x + w / 2), (y + h / 2), (w * h)]  # TODO maybe without returning x, y, w, h?
