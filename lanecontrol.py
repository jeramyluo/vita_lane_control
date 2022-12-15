'''
  File name: lanecontrol.py
  Author(s):  Jeramy Luo - entire file
  Purpose: Main control loop for the Visual Task Specification for Vehicle Lane Control model.
'''

import cv2

from grabscreen import process_input
from ultrafastLaneDetector import UltrafastLaneDetector, ModelType
from visualtaskspec import vistaskspec
from pid import pdcontroller

if __name__ == "__main__":
  # initializing lane detection model
  lane_detector = UltrafastLaneDetector("models/tusimple.onnx", ModelType.TUSIMPLE)
  # initializing visual task specification class
  vts = vistaskspec()
  # initializing pd control class
  controller = pdcontroller()

  while True:
    # processing input
    frame = process_input()
    # detecting the lanes
    output_img, lanes_pts, lanes_detected  = lane_detector.detect_lanes(frame)
    # acquiring error term
    err = vts.get_error(lanes_pts, lanes_detected, output_img, controller.get_mode())
    # updating pid controller if valid error received
    if err != None:
      controller.update_controls(err)
    # updating controls from control window
    controller.update_trackbars()
    # showing windows
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break