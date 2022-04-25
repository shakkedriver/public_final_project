def dice_coefficient(bounding_box1, bounding_box2):
    """

    @param bounding_box1:  [x,y,w,h]
    @param bounding_box2:
    @return: gauge the similarity of two images: Area of overlap / Area of Union
    """
    x_inteval1 = [bounding_box1[0], bounding_box1[0] + bounding_box1[2]]
    x_inteval2 = [bounding_box2[0], bounding_box2[0] + bounding_box2[2]]
    y_inteval1 = [bounding_box1[1], bounding_box1[1] + bounding_box1[3]]
    y_inteval2 = [bounding_box2[1], bounding_box2[1] + bounding_box2[3]]
    overlap_area = get_overlap_interval(x_inteval1,x_inteval2)*get_overlap_interval(y_inteval1,y_inteval2)
    bb1_area = bounding_box1[2]*bounding_box1[3]
    bb2_area = bounding_box2[2] * bounding_box2[3]
    return 2*overlap_area/(bb1_area+bb2_area)


def get_overlap_interval(interval1, interval2):
    """

    @param interval1: [x1, x1 + w1]
    @param interval2: [x2, x2 + w2]
    @return:  overlap interval
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


def test_ovelap():
    inter1 = [30, 90]
    inter2 = [40, 100]
    assert get_overlap_interval(inter1, inter2) == 50
    assert get_overlap_interval(inter2, inter1) == 50
    inter1 = [30, 90]
    inter2 = [40, 80]
    assert get_overlap_interval(inter1, inter2) == 40
    assert get_overlap_interval(inter2, inter1) == 40
    inter1 = [30, 90]
    inter2 = [90, 240]
    assert get_overlap_interval(inter1, inter2) == 0
    assert get_overlap_interval(inter2, inter1) == 0
    inter1 = [30, 90]
    inter2 = [91, 240]
    assert get_overlap_interval(inter1, inter2) == 0
    assert get_overlap_interval(inter2, inter1) == 0
def test_dice():
    bb1 = [100,100,50,50]
    bb2 = [125,125,50,50]
    assert dice_coefficient(bb1,bb2) == 2*(25**2)/5000
    assert dice_coefficient(bb2, bb1) == 2 * (25 ** 2) / 5000
    assert dice_coefficient(bb1, bb1) == 1
    bb2 = [0, 0, 50, 50]
    assert dice_coefficient(bb1, bb2) == 0
    assert dice_coefficient(bb2, bb1) == 0
    bb2 = [125, 125, 10, 10]
    assert dice_coefficient(bb2, bb1) == 2 * (10** 2) / 2600

if __name__ == '__main__':
    test_ovelap()
    test_dice()
