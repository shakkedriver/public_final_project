import numpy as np
import time


class PID:
    """
    this class implements a pid control module that can get three constants (gains) and a target goal and allow the user
    to get the value neesery to input to the system in order to stabilize it closer to the target value.
    you can read more about the pid model here : https://en.wikipedia.org/wiki/PID_controller
    """
    def __init__(self, Kp, Ki, Kd, targetVal, limit=None):
        """

        :param Kp: the size of the part of the adjustments we want to make in each call to update that is proportional to
        the error
        :param Ki: the size of the part of the adjustments we want to make in each call to update that is proportional to
        the integral of the error across time. the idea is that if we are above the goal for a long time the model would
        return larger adjustments, so we would not be biased to one side for a long time.
        :param Kd: the size of the part of the adjustments we want to make in each call to update that is proportional to
        the derivetiv of the error. if the error got bigger we would want to aplay more force back to the system
        :param targetVal: the desired set point
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
        self.I = self.I + (self.Ki * error * (t - self.pTime))
        D = (self.Kd * (error - self.pError)) / t

        result = P + self.I + D

        if self.limit is not None:
            result = float(np.clip(result, self.limit[0], self.limit[1]))
        self.pError = error
        self.ptime = time.time()

        return result