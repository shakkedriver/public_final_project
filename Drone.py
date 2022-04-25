import threading
import multiprocessing
import time
from datetime import datetime

import keyboard

import Detection
import cv2
import numpy as np
from djitellopy import tello
import Tracker
import constants

now = datetime.now()


class Drone(tello.Tello):
    """
    this is a drone class we inherit from the tello.Tello class and added data and functionality to our needs
    """

    def __init__(self):
        """
        calls the super constructor and runs the code needed for use of the object
        """

        self.BUFFER_SIZE = 10000

        # connecting to Tello
        super().__init__(retry_count=6)
        self.connect()
        print(self.get_battery())
        self.streamoff()
        self.streamon()

        # synchronization
        self.buffer_mutex = threading.RLock()  # only one thread can access the buffer
        self.fillCount = threading.Semaphore(0)  # counts how many frames are in the buffer
        self.emptyCount = threading.Semaphore(self.BUFFER_SIZE)  # prevents threads from accessing the buffer when

        # initializing different classes
        self.frames_receiver = self.FramesReceiver(self)
        self.video_saver = self.VideoSaver(self)
        self.detector = Detection.ObjectsDetector("yolov3.cfg", "yolov3.weights")

        # initializing Tracker
        self.tracker = Tracker.ObjectTracking((0.19, 1e-10, 0, constants.FRAME_SHAPE[0] // 2),
                                              (1, 0, 0.1, constants.FRAME_SHAPE[1] // 1.9),
                                              (200, 0, 0, 0.25))

        # initializing threads
        self.saver_thread = threading.Thread(target=self.video_saver.create_video_loop, name='saver_thread')
        self.saver_thread.start()
        self.receiver_thread = threading.Thread(target=self.frames_receiver.readframes, name='receiver_thread')
        self.receiver_thread.start()

    class FramesReceiver:
        """
        this class receives frames from the drone and stored them in a array
        """

        def __init__(self, drone):
            """
            gets the drone and inits all the object we need for the task
            :param drone: the drone
            """
            self.drone = drone
            self.image_buffer = []
            self.VideoCap = self.drone.get_video_capture()

        def readframes(self):
            """
            runs in a loop and reads new frames from the drone. this function should be called in a new thread
            :return: None
            """
            while True:
                ret, img = self.VideoCap.read()
                if ret:
                    img = cv2.resize(img, constants.FRAME_SHAPE)
                    self.drone.emptyCount.acquire()
                    self.drone.buffer_mutex.acquire()

                    self.image_buffer.append(img)

                    self.drone.buffer_mutex.release()
                    self.drone.fillCount.release()

        def getFrame(self, consume=True):
            """
            allow reading from the array buffer safely if consume is true we would pop the beginning of the buffer
            else we would just read the last frame
            :param consume:
            :return:
            """
            if consume:
                self.drone.fillCount.acquire()
                self.drone.buffer_mutex.acquire()
                img = self.image_buffer.pop(0)
                self.drone.buffer_mutex.release()
                self.drone.emptyCount.release()
                return img
            else:
                self.drone.fillCount.acquire()
                self.drone.buffer_mutex.acquire()
                img = self.image_buffer[-1]
                self.drone.buffer_mutex.release()
                self.drone.fillCount.release()
                return img.copy()

    class VideoSaver:
        """
        this a local class that deals with saving videos from  the frames_receiver of the drone and storing them
        """

        def __init__(self, drone):
            """
            gets the drone object for the class and creates all the objects necessary for saving a video
            :param drone: the drone
            """
            self.drone = drone
            self.video_writer = cv2.VideoWriter(f'{now.strftime("%H:%M:%S")}.avi',
                                                cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 30, constants.FRAME_SHAPE)

        def create_video_loop(self):
            """
            reads from the array in a loop and saves the video when q is pressed video would be saved. this function is called with a new thread
            :return:
            """
            while True:
                img = self.drone.frames_receiver.getFrame()
                if cv2.waitKey(5) & 0xFF == ord('q'):
                    self.drone.land()
                    self.video_writer.release()
                    cv2.destroyAllWindows()
                    break
                # cv2.imshow("Image", img)
                self.video_writer.write(img)

    def polygon(self, num_corners: int, radius_in_cm):
        """
        move the drone in a Regular polygon shape while facing to the center of the polygon
        :param num_corners: the number of corners for the polygon
        :param radius_in_cm: the radius in cm for the circle bounding the polygon
        :return:None
        """
        for i in range(num_corners):
            self.rotate_clockwise(int(360 / num_corners))
            self.move_left(abs(int(radius_in_cm * np.sin(360 / num_corners) * 2)))

    def getFrame(self):
        """
        gets the latest image received from the drone
        """
        return self.frames_receiver.getFrame(consume=False)
    def emergency_landing_check(self):
        if keyboard.is_pressed('q'):
            cv2.destroyAllWindows()
            self.send_rc_control(0, 0, 0, 0)
            self.land()
            exit(1)

    def track(self):
        """

        """
        while True:
            bbox = self.detector.find_center(self.getFrame())
            xVal, yVal, zVal = self.tracker.get_rc_commend(bbox)
            self.send_rc_control(0, -zVal, -yVal, xVal)
            self.emergency_landing_check()


def dice_coefficient(bounding_box1, bounding_box2):
    """

    @param bounding_box1:  [x,y,w,h]
    @param bounding_box2:
    @return: gauge the similarity of two images: Area of overlap / Area of Union
    """
    x_inteval1 = [bounding_box1[0], bounding_box1[0] + bounding_box1[2]]
    x_inteval2 = [bounding_box2[0], bounding_box2[0] + bounding_box2[2]]
    y_inteval1 = [bounding_box1[1], bounding_box1[1] + bounding_box1[3]]
    y_inteval2 = [bounding_box2[1], bounding_box2[1] + bounding_box2[3]]
    overlap_area = get_overlap_interval(x_inteval1, x_inteval2) * get_overlap_interval(y_inteval1, y_inteval2)
    bb1_area = bounding_box1[2] * bounding_box1[3]
    bb2_area = bounding_box2[2] * bounding_box2[3]
    return 2 * overlap_area / (bb1_area + bb2_area)


def get_overlap_interval(interval1, interval2):
    """

    @param interval1: [x1, x1 + w1]
    @param interval2: [x2, x2 + w2]
    @return:  overlap interval
    """
    if interval1[0] < interval2[0]:
        interval_a = interval1
        interval_b = interval2
    else:
        interval_b = interval1
        interval_a = interval2
    if interval_b[0] > interval_a[1]:
        return 0
    elif interval_b[1] < interval_a[1]:
        return interval_b[1] - interval_b[0]
    else:
        return interval_a[1] - interval_b[0]


def test_ovelap():
    inter1 = [30, 90]
    inter2 = [40, 100]
    assert get_overlap_interval(inter1, inter2) == 50
    assert get_overlap_interval(inter2, inter1) == 50
    inter1 = [30, 90]
    inter2 = [40, 80]
    assert get_overlap_interval(inter1, inter2) == 40
    assert get_overlap_interval(inter2, inter1) == 40
    inter1 = [30, 90]
    inter2 = [90, 240]
    assert get_overlap_interval(inter1, inter2) == 0
    assert get_overlap_interval(inter2, inter1) == 0
    inter1 = [30, 90]
    inter2 = [91, 240]
    assert get_overlap_interval(inter1, inter2) == 0
    assert get_overlap_interval(inter2, inter1) == 0


def test_dice():
    bb1 = [100, 100, 50, 50]
    bb2 = [125, 125, 50, 50]
    assert dice_coefficient(bb1, bb2) == 2 * (25 ** 2) / 5000
    assert dice_coefficient(bb2, bb1) == 2 * (25 ** 2) / 5000
    assert dice_coefficient(bb1, bb1) == 1
    bb2 = [0, 0, 50, 50]
    assert dice_coefficient(bb1, bb2) == 0
    assert dice_coefficient(bb2, bb1) == 0
    bb2 = [125, 125, 10, 10]
    assert dice_coefficient(bb2, bb1) == 2 * (10 ** 2) / 2600


if __name__ == '__main__':
    test_ovelap()
    test_dice()
