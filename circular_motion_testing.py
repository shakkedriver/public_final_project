import sys

from Drone import Drone
from Tracker import ObjectTracking
import constants
import cv2
tracker = ObjectTracking(pid_values_x=(0.25, 0, 0.1, constants.FRAME_SHAPE[0] // 2),
                         pid_values_y=(1, 0, 0.1, constants.FRAME_SHAPE[1] // 1.9),
                         pid_values_z=(100, 0, 0.3, 0.025))
if __name__ == '__main__':
    drone = Drone()
    drone.takeoff()
    drone.move_up(30)
    while True:
        bbox = drone.detector.find_center(drone.getFrame())
        xVal, yVal, zVal = tracker.get_rc_commend(bbox)
        drone.send_rc_control(50, -zVal, -yVal, xVal)
        if cv2.waitKey(5) & 0xFF == ord('q'):
            drone.land()
            cv2.destroyAllWindows()
            drone.send_rc_control(0, 0, 0, 0)
            break
    sys.exit(1)



