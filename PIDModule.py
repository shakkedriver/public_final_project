import numpy as np
import time



class PID:
    def __init__(self, Kp, Ki, Kd, targetVal, limit=None):
        """

        :param pidVals: include the gain values of KP, KI, KD
        :param targetVal: the desired setpoint
        :param limit: limitation of the drone
        """
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.targetVal = targetVal
        self.pError = 0
        self.limit = limit
        self.I = 0
        self.pTime = 0

    def update(self, cVal):
        """

        :param cVal: the object current position
        :return: update pidVal - the gain values of KP, KI, KD
        """
        t = time.time() - self.pTime
        error = cVal - self.targetVal
        P = self.Kp * error
        self.I = self.I + (self.Ki * error * (t-self.pTime))
        D = (self.Kd * (error - self.pError)) / t

        result = P + self.I + D

        if self.limit is not None:
            result = float(np.clip(result, self.limit[0], self.limit[1]))
        self.pError = error
        self.ptime = time.time()

        return result
