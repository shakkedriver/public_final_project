from PIDModule import PID
import Consten

class ObjectTracking:
    def __init__(self, pid_values_x, pid_values_y, pid_values_z):
        """
        This function creates the tracker object.
        Gets as an input a 4-tuple where each tuple correspond to a direction (x,y,z).

        @param pid_values_x: x direction 4-tuple (Kp, Ki, Kd, targetVal)
        @param pid_values_y: height 4-tuple (Kp, Ki, Kd, targetVal)
        @param pid_values_z: forward and backwards 4-tuple (Kp, Ki, Kd, targetVal)
        """
        self.xPID = PID(Kp=pid_values_x[0], Ki=pid_values_x[1], Kd=pid_values_x[2], targetVal=pid_values_x[3],
                        limit=[-100, 100])  # x direction
        self.yPID = PID(Kp=pid_values_y[0], Ki=pid_values_y[1], Kd=pid_values_y[2], targetVal=pid_values_y[3],
                        limit=[-100, 100])  # height
        self.zPID = PID(Kp=pid_values_z[0], Ki=pid_values_z[1], Kd=pid_values_z[2], targetVal=pid_values_z[3],
                        limit=[-100, 100])  # forward and backwards

    def get_rc_commend(self, bbox):
        """
        This function computes the values that we will return to the rc control inorder to move the drone accordingly
        @param bbox: [x, y, w, h, cx, cy, area]
        @return: xVal, yVal, zVal
        """
        xVal = 0
        yVal = 0
        zVal = 0
        if bbox:
            [x, y, w, h, cx, cy, area] = bbox
            z_ratio = area / Consten.FRAME_SIZE
            cx, cy = int(cx), int(cy)
            xVal = int(self.xPID.update(cx))
            yVal = int(self.yPID.update(cy))
            zVal = int(self.zPID.update(z_ratio))
        return xVal, yVal, zVal
