from Drone import Drone
import cv2
import keyboard

if __name__ == "__main__":
    myDrone = Drone()
    myDrone.takeoff()
    myDrone.move_up(20)
    # time.sleep(1)
    # myDrone.polygon(12, 200)
    myDrone.track_test()
    # myDrone.land()
