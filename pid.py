'''
  File name: pid.py
  Author(s):  Jeramy Luo - entire file
  Purpose: Contains the pdcontroller class for the lane control system.
'''

import numpy as np
import cv2
import pyvjoy
import time

class pdcontroller():
    def __init__(self):
        # creating the control panel
        self.create_controls()

        # creating the virtual joystick class
        self.j = pyvjoy.VJoyDevice(1)

        # setting initial gains
        self.kp = 0
        self.kd = 0
        self.skp = 0
        self.speed = 0

        # control panel display
        self.display = np.zeros([100,600,3], np.uint8)

        # derivative term
        self.last = 0

        # turn rate
        self.t = 0

        # speed
        self.final_speed = 0

        # fps timer
        self.last_time = time.time()

        # mode for task
        self.mode = 0

    def create_controls(self):
        # creates the window and taskbar for the control panel

        cv2.namedWindow("controls")
        cv2.resizeWindow("controls", 500, 500)
        cv2.createTrackbar("turn_kp", "controls", 0, 100, self.null)
        cv2.createTrackbar("turn_kd", "controls", 0, 100, self.null)
        cv2.createTrackbar("s_kp", "controls", 0, 100, self.null)
        cv2.createTrackbar("speed", "controls", 0, 10, self.null)
        cv2.createTrackbar("mode", "controls", 0, 5, self.null)
    
    def update_trackbars(self):
        # updating the controls on the control panel

        self.kp = 1/10000 * cv2.getTrackbarPos("turn_kp", "controls")
        self.kd = 1/5000 * cv2.getTrackbarPos("turn_kd", "controls")
        self.skp = 0.2 * cv2.getTrackbarPos("s_kp", "controls")
        self.speed = 0.1 * cv2.getTrackbarPos("speed", "controls")
        self.mode = cv2.getTrackbarPos("mode", "controls")
        self.show()
    
    def update_controls(self, error):
        # main loop of the pid controller; takes in error and finds the turn rate to control the vehicle

        # calculating derivative term
        d = -error - self.last

        # updating last
        self.last = -error

        # updating turn rate
        self.t = -(-error * self.kp + d * self.kd)

        # turning the vehicle
        self.turn()

        # clearing image
        self.display = np.zeros([100,600,3], np.uint8)

    def turn(self):
        # finds the speed rate and calls the virtual joystick

        # defining max value of virtual joystick
        MAX_VJOY = 32767

        # finding speed coefficient
        self.final_speed = self.p_speed()
        
        # sending virtual joystick speed command
        self.j.set_axis(pyvjoy.HID_USAGE_SL0, int(MAX_VJOY*self.final_speed))

        # sending virtual joystick turn command
        self.j.set_axis(pyvjoy.HID_USAGE_X, int(MAX_VJOY*(1/2 + self.t)))

    def p_speed(self):
        # finds the speed coefficient

        speed = self.speed - self.skp*np.abs(self.t)
        # trimming ends
        if speed < 0:
            speed = 0
        if speed > 1:
            speed = 1
        return speed
    
    def show(self):
        # defining task list:
        task_list = ["point2point", "point2line", "cent2point", "cent2line", "parlines", "line2line"]

        # updates the display on the control panel

        # calculating fps
        fps = 1/(time.time() - self.last_time)

        # updating last_time
        self.last_time = time.time()

        # displaying fps
        cv2.putText(self.display, f"FPS: {int(fps)}", (400, 35),cv2.FONT_HERSHEY_SIMPLEX,1, (255, 255, 255), 2, cv2.LINE_AA)

        # displaying L or R and turn rate in %
        if self.t < 0:
            cv2.putText(self.display, f"L: {np.abs(round(self.t/0.5*100, 1))}%", (5, 35),cv2.FONT_HERSHEY_SIMPLEX,1, (255, 0, 0), 2, cv2.LINE_AA)
        if self.t > 0:
            cv2.putText(self.display, f"R: {np.abs(round(self.t/0.5*100, 1))}%", (5, 35),cv2.FONT_HERSHEY_SIMPLEX,1, (0, 0, 255), 2, cv2.LINE_AA)

        # displaying speed %
        cv2.putText(self.display, f"S: {np.abs(round(self.final_speed*100, 1))}%", (200, 35),cv2.FONT_HERSHEY_SIMPLEX,1, (255, 255, 255), 2, cv2.LINE_AA)

        # displaying visual task
        cv2.putText(self.display, f"Mode: {task_list[self.mode]}", (5, 85),cv2.FONT_HERSHEY_SIMPLEX,1, (255, 255, 255), 2, cv2.LINE_AA)

        # showing control panel display
        cv2.imshow("controls", self.display)
    
    def get_mode(self):
        # returns mode that gives specific visual task
        return int(self.mode)
    
    def null(self, x):
        # null function for use in opencv trackbar
        pass