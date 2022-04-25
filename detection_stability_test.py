import os
import time
import Drone
import numpy as np
import matplotlib.pyplot as plt


def dice_coefficient(bounding_box1, bounding_box2):
    """

    @param bounding_box1:  [x,y,w,h]
    @param bounding_box2:
    @return: gauge the similarity of two images: Area of overlap / Area of Union
    """
    x_interval1 = [bounding_box1[0], bounding_box1[0] + bounding_box1[2]]
    x_interval2 = [bounding_box2[0], bounding_box2[0] + bounding_box2[2]]
    y_interval1 = [bounding_box1[1], bounding_box1[1] + bounding_box1[3]]
    y_interval2 = [bounding_box2[1], bounding_box2[1] + bounding_box2[3]]
    overlap_area = get_overlap_interval(x_interval1, x_interval2) * get_overlap_interval(y_interval1, y_interval2)
    bb1_area = bounding_box1[2] * bounding_box1[3]
    bb2_area = bounding_box2[2] * bounding_box2[3]
    return 2 * overlap_area / (bb1_area + bb2_area)


def get_overlap_interval(interval1, interval2):
    """

    @param interval1: [x1, x1 + w1]
    @param interval2: [x2, x2 + w2]
    @return: overlap interval
    """
    if interval1[0] < interval2[0]:
        interval_a = interval1
        interval_b = interval2
    else:
        interval_b = interval1
        interval_a = interval2
    if interval_b[0] > interval_a[1]:
        return 0
    elif interval_b[1] < interval_a[1]:
        return interval_b[1] - interval_b[0]
    else:
        return interval_a[1] - interval_b[0]


def test_static_person():
    myDrone = Drone.Drone()
    bbox_counter, no_bbox_counter, frame_count, array_bbox = myDrone.track_test()
    print(f"number of times the neural network was called on a frame {bbox_counter}\n",
          f"number of times the network didn't detect a person {no_bbox_counter}\n",
          f"number of frames received in the time interval {frame_count}")
    # analyse_dice_cof(array_bbox, "Static Person and Static Drone")
    # analyse_dice_cof(array_bbox, "Moving Person and Static Drone")
    analyse_dice_cof(array_bbox, "Static Person and Moving Drone")


def analyse_dice_cof(array_bbox, test_name=""):
    d = [dice_coefficient(array_bbox[i], array_bbox[i + 1]) for i in range(len(array_bbox) - 1)]
    deriv_d = [d[i + 1] - d[i] for i in range(len(d) - 1)]
    d_mean = np.mean(d)
    d_var = np.var(d)
    deriv_d_mean = np.mean(deriv_d)
    deriv_d_var = np.var(deriv_d)
    np.save("d_" + test_name, d)
    np.save("deriv_d_" + test_name, deriv_d)
    graph_for_test(test_name, d, deriv_d)


def graph_for_test(test_name, d, deriv_d):
    hist, _ = np.histogram(d, bins=10, range=[0, 1])
    x = np.arange(len(hist)) * 0.1
    plt.bar(x, hist, 0.05)
    plt.title("Dice Coefficient Histogram\n for " + test_name)

    plt.savefig(test_name + "_histogram.png")
    plt.clf()
    plt.plot(d)
    plt.title("Dice Coefficient as a Function of Time\n for " + test_name)
    plt.ylabel("dice coefficient")

    plt.xticks(color='w')
    plt.savefig(test_name + "_scatter.png")


if __name__ == '__main__':
    print(test_static_person())
