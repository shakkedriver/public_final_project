# from Drone import Drone
# import cv2
#
# if __name__ == "__main__":
#     myDrone = Drone()
#     myDrone.takeoff()
#     myDrone.move_up(20)
#     # time.sleep(1)
#     # myDrone.polygon(12, 200)
#     myDrone.track()
#     if cv2.waitKey(5) & 0xFF == ord('q'):
#         myDrone.land()
#         cv2.destroyAllWindows()
#         myDrone.send_rc_control(0, 0, 0, 0)