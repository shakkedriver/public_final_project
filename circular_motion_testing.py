from Drone import Drone
from Tracker import ObjectTracking
import constants
tracker = ObjectTracking(pid_values_x=(0.4, 0, 0, constants.FRAME_SHAPE[0] // 2),
                         pid_values_y=(1, 0, 0.1, constants.FRAME_SHAPE[1] // 1.9),
                         pid_values_z=(100, 0, 0, 0.08))
if __name__ == '__main__':
    drone = Drone()
    drone.takeoff()
    drone.move_up(30)
    while True:
        bbox = drone.detector.find_center(drone.get_frame())
        xVal, yVal, zVal = tracker.get_rc_commend(bbox)
        drone.send_rc_control(40, -zVal, -yVal, xVal)
        # drone.emergency_landing_check()



