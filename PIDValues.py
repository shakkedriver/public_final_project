from Drone import Drone
import PIDModule


hi, wi, = 480, 640

#                      P   I  D
xPID = PIDModule.PID(0.22, 0, 0.1, wi // 2)  # x direction
yPID = PIDModule.PID(0.27, 0, 0.1, hi // 2)  # height
zPID = PIDModule.PID(0.003, 0, 0.003, 12000, limit=[-20, 15])  # forward and backwards

drone = Drone()
detector = drone.detector

while True:
    img = drone.getFrame()
    img, objects = detector.center_detect(img)
    nearest = detector.find_nearest(objects)

    xVal = 0
    yVal = 0
    zVal = 0
    if nearest != ():
        x, y, w, h, cx, cy, area = nearest.reshape((-1))
        cx, cy = int(cx), int(cy)
        xVal = int(xPID.update(cx))
        yVal = int(yPID.update(cy))
        zVal = int(zPID.update(int(area)))
    # drone.send_rc_control(0, - zVal, -yVal, xVal)
    drone.send_rc_control(0, 0, 0, xVal)

