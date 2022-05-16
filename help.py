import torch
import cv2
# Model
model = torch.hub.load('ultralytics/yolov5', 'yolov5n')  # or yolov5m, yolov5l, yolov5x, custom
import yolov5.models.common

# model = yolov5.models.common.DetectMultiBackend()
# Images

cap = cv2.VideoCapture(0)
# img = 'https://ultralytics.com/images/zidane.jpg'  # or file, Path, PIL, OpenCV, numpy, list
while True:
    _, img = cap.read()

    img = cv2.resize(img, (1280, 720))

    # Inference
    results = model(img)

    # Results
    results.print()  # or .show(), .save(), .crop(), .pandas(), etc.