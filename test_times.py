import Drone
import time


def test_computer_drone_computer(drone):
    total = 0
    number_of_iter = 1000
    for i in range(number_of_iter):
        t1 = time.time()
        drone.detector.find_center(drone.getFrame())
        t2 = time.time()
        total += t2 - t1

    return total / number_of_iter


if __name__ == '__main__':
    myDrone = Drone.Drone()
    print(test_computer_drone_computer(myDrone))
