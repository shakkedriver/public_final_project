from Drone import Drone
import PIDModule
from Drone import FRME_Shape

if __name__ == '__main__':


    #                      P   I  D
    xPID = PIDModule.PID(Kp=0.25, Ki=0, Kd=0,targetVal= FRME_Shape[0] // 2,limit=[-100, 100])  # x direction
    yPID = PIDModule.PID(1, 0, 0.1, FRME_Shape[1] // 1.9,limit=[-100, 100])  # height
    zPID = PIDModule.PID(200, 0, 0, 0.15, limit=[-100, 100])  # forward and backwards

    drone = Drone()
    detector = drone.detector


    drone.takeoff()
    drone.move_up(50)
    while True:
        img = drone.getFrame()
        # img, objects = detector.center_detect(img)
        # nearest = detector.find_nearest(objects)
        bbox = detector.find_center(img)
        xVal = 0
        yVal = 0
        zVal = 0
        if cv2.waitKey(5) & 0xFF == ord('q'):
            drone.land()
            cv2.destroyAllWindows()
            drone.send_rc_control(0, 0, 0, 0)
            break
        if bbox:
            [x, y, w, h, cx, cy, area] = bbox
            z_ratio = area/(FRME_Shape[0]*FRME_Shape[1])
            cx, cy = int(cx), int(cy)
            xVal = int(xPID.update(cx))
            yVal = int(yPID.update(cy))
            zVal = int(zPID.update(z_ratio))
        # drone.send_rc_control(0, - zVal, -yVal, xVal)
        # drone.send_rc_control(0, zVal, -yVal, xVal)
        drone.get_height()
        # drone.send_rc_control(0, -zVal,-yVal, xVal)
        drone.send_rc_control(0, -zVal, -yVal, xVal)
