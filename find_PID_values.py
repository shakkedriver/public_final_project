from djitellopy import tello
import cv2
import PIDModule

import Detection

# detector = Detection.ObjectsDetector("haarcascade_fullbody.xml")
detector = Detection.ObjectsDetector("haarcascade_frontalface_default.xml")

hi, wi, = 480, 640

#                      P   I  D
xPID = PIDModule.PID(0.22, 0, 0.1, wi // 2)  # x direction
yPID = PIDModule.PID(0.27, 0, 0.1, hi // 2)  # height
zPID = PIDModule.PID(0.003, 0, 0.003, 12000, limit=[-20, 15])  # forward and backwards

# myPlotX = PlotModule.LivePlot(yLimit=[-100, 100], char='X')
# myPlotY = PlotModule.LivePlot(yLimit=[-100, 100], char='Y')
# myPlotZ = PlotModule.LivePlot(yLimit=[-100, 100], char='Z')

me = tello.Tello()
me.connect()
print(me.get_battery())
me.streamoff()
me.streamon()
me.takeoff()
me.move_up(70)


# def stackImages(_imgList, cols, scale):
#     """
#     Stack Images together to display in a single window
#     :param _imgList: list of images to stack
#     :param cols: the num of img in a row
#     :param scale: bigger~1+ ans smaller~1-
#     :return: Stacked Image
#     """
#     imgList = copy.deepcopy(_imgList)
#
#     # make the array full by adding blank img, otherwise the openCV can't work
#     totalImages = len(imgList)
#     rows = totalImages // cols if totalImages // cols * cols == totalImages else totalImages // cols + 1
#     blankImages = cols * rows - totalImages
#
#     width = imgList[0].shape[1]
#     height = imgList[0].shape[0]
#     imgBlank = np.zeros((height, width, 3), np.uint8)
#     imgList.extend([imgBlank] * blankImages)
#
#     # resize the images
#     for i in range(cols * rows):
#         imgList[i] = cv2.resize(imgList[i], (0, 0), None, scale, scale)
#         if len(imgList[i].shape) == 2:
#             imgList[i] = cv2.cvtColor(imgList[i], cv2.COLOR_GRAY2BGR)
#
#     # put the images in a board
#     hor = [imgBlank] * rows
#     for y in range(rows):
#         line = []
#         for x in range(cols):
#             line.append(imgList[y * cols + x])
#         hor[y] = np.hstack(line)
#     ver = np.vstack(hor)
#     return ver


while True:
    # _, img = cap.read()
    img = me.get_frame_read().frame

    img = cv2.resize(img, (wi, hi))
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

        # img = xPID.draw(img, [cx, cy])
        # img = yPID.draw(img, [cx, cy], 1)

        # imgPlotX = myPlotX.update(xVal)
        # imgPlotY = myPlotY.update(yVal)
        # imgPlotZ = myPlotZ.update(zVal)

        # imgStacked = stackImages([img, imgPlotX, imgPlotY, imgPlotZ], 2, 0.6)

    # else:
        # imgStacked = stackImages([img], 1, 0.75)

    me.send_rc_control(0, - zVal, -yVal, xVal)
    # me.send_rc_control(0, -zVal, 0, 0)
    # cv2.imshow("Image Stacked", imgStacked)

    if cv2.waitKey(5) & 0xFF == ord('q'):
        me.land()
        break
cv2.destroyAllWindows()
