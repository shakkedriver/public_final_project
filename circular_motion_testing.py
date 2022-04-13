import sys
import keyboard
from Drone import Drone
from Tracker import ObjectTracking
import constants
import cv2
tracker = ObjectTracking(pid_values_x=(0.25, 1e-12, 0.1, constants.FRAME_SHAPE[0] // 2),
                         pid_values_y=(1, 0, 0.1, constants.FRAME_SHAPE[1] // 1.9),
                         pid_values_z=(200, 0, 0.3, 0.075))
if __name__ == '__main__':
    drone = Drone()
    drone.takeoff()
    drone.move_up(30)
    while True:
        bbox = drone.detector.find_center(drone.getFrame())
        if not bbox:
            drone.send_rc_control(0, 0, 0, 0)

        xVal, yVal, zVal = tracker.get_rc_commend(bbox)
        drone.send_rc_control(50, -zVal, -yVal, xVal)
        if keyboard.is_pressed('q'):
            cv2.destroyAllWindows()
            drone.send_rc_control(0, 0, 0, 0)
            drone.land()
            sys.exit(1)





