import threading
import time
from datetime import datetime
import Detection
import cv2
import numpy as np
from djitellopy import tello

FRME_Shape = (400, 300)
now = datetime.now()


class Drone(tello.Tello):
    """
    this is a drone class we inherit from the tello.Tello class and added data and functionality to our needs
    """

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
                                                cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 30, FRME_Shape)

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
                cv2.imshow("Image", img)
                self.video_writer.write(img)

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
                    img = cv2.resize(img, FRME_Shape)
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
        return self.frames_receiver.getFrame(consume=False)


if __name__ == "__main__":
    myDrone = Drone()
    time.sleep(40)

    myDrone.takeoff()
    myDrone.move_up(300)
    time.sleep(1)
    myDrone.polygon(12, 200)
    myDrone.send_rc_control(0, 0, 0, 0)
    myDrone.land()

    time.sleep(10)
