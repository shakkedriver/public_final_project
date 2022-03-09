import cv2
import numpy as np


class PersonDetector:
    """
    Find people in realtime using the haarcascade_fullbody
    """

    def __init__(self, haarcascade_file):
        """

        :param haarcascade_file:
        """
        # "haarcascade_fullbody.xml"
        self.fullBodyCascade = cv2.CascadeClassifier(haarcascade_file, )

    def detect(self, img):
        """

        :param img:
        :return:
        """
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return self.fullBodyCascade.detectMultiScale(imgRGB, 1.2, 1)

    def center_detect(self, img):
        """
        Find people in an image and return the bbox info
        :param img: Image to find the people in.
        :return: Image, Bounding Box list.
        """
        people = self.detect(img)
        bboxs = []
        for (x, y, w, h) in people:
            bboxs = [x, y, w, h]
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            # the center point and the area
            bbox = [x, y, w, h]
            cx = x + w / 2
            cy = y + h / 2
            area = w * h
            bboxInfo = {"area": area, "bbox": bbox, "center": (cx, cy)}
            bboxs.append(bboxInfo)
        return img, bboxs


class YOLODetector:
    def __init__(self, config_file, whightes_file):
        self.net = cv2.dnn.readNetFromDarknet(config_file, whightes_file)
        self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
        self.ln = self.net.getLayerNames()
        self.ln = [self.ln[i - 1] for i in self.net.getUnconnectedOutLayers()]

    def detect(self, img, prob=.5):
        H, W = img.shape[:2]
        blob = cv2.dnn.blobFromImage(img, 1 / 255.0, (416, 416), swapRB=True, crop=False)
        self.net.setInput(blob)
        outputs = self.net.forward(self.ln)
        outputs = np.vstack(outputs)
        outputs = outputs[:, :6]
        outputs = outputs[np.where(outputs[:, 5] > prob)]
        if outputs.shape[0] != 0:
            outputs = outputs[np.argmax(outputs[:, 5])]
        outputs = outputs.reshape((-1, 6))
        outputs[:, 0:4] *= np.array([W, H, W, H])
        outputs[:, 0] -= outputs[:, 2] // 2
        outputs[:, 1] -= outputs[:, 3] // 2

        return outputs
