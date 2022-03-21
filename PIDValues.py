from Drone import Drone
import PIDModule
import cv2
import Consten

if __name__ == '__main__':

    xPID = PIDModule.PID(Kp=0.25, Ki=0, Kd=0, targetVal=Consten.FRAME_SHAPE[0] // 2, limit=[-100, 100])  # x direction
    yPID = PIDModule.PID(1, 0, 0.1, Consten.FRAME_SHAPE[1] // 1.9, limit=[-100, 100])  # height
    zPID = PIDModule.PID(200, 0, 0, 0.25, limit=[-100, 100])  # forward and backwards

    drone = Drone()
    detector = drone.detector

    # drone.takeoff()
    # drone.move_up(50)
    frame_size = (Consten.FRAME_SHAPE[0] * Consten.FRAME_SHAPE[1])
    move_left = False
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
            z_ratio = area / frame_size
            cx, cy = int(cx), int(cy)
            xVal = int(xPID.update(cx))
            yVal = int(yPID.update(cy))
            zVal = int(zPID.update(z_ratio))
        # drone.get_height()

        drone.send_rc_control(15, -zVal, -yVal, xVal)



