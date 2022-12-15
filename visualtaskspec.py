'''
  File name: visualtaskspec.py
  Author(s):  Jeramy Luo - entire file
  Purpose: Contains the visual task specification class for the lane control system.
'''

import numpy as np
import cv2

from shapely.geometry import Polygon

class vistaskspec():
    def __init__(self):
        # initializing task list
        self.task_list = ["point2point", "point2line", "cent2point", "cent2line", "parlines", "line2line"]
    
    def get_error(self, lane_points, detected, output_img, mode):
        # this function calls the function corresponding to the defined visual specification task

        # checking if adjacent lanes are detected:
        if detected[1] and detected[2] == 1:
            # defining the visual task based on the mode
            visual_task = getattr(self, f"{self.task_list[mode]}")
            # extracting left and right lane
            left_lane = np.array(lane_points[1]).transpose()
            right_lane = np.array(lane_points[2]).transpose()

            # finding screen width
            width = output_img.shape[1]
            # calling function corresponding to task
            error, output_img = visual_task(left_lane, right_lane, width, output_img)
            # showing output image
            cv2.imshow("Lane Detection", output_img[0:620, 320:960])
            # returning error and output image
            return error
        # if lanes aren't detected, shows unmodified output image and returns None for error
        else:
            cv2.imshow("Lane Detection", output_img[0:620, 320:960])
            return None
    
    def get_centroid(self, left_lane, right_lane):
        # this function finds the centroid of lane polygon

        points = np.vstack((left_lane.transpose(),np.flipud(right_lane.transpose())))
        p1 = Polygon(points)
        return np.array(p1.centroid)

    def point2point(self, left_lane, right_lane, width, output_img):
        # finds the point to point visual task specification

        # finding y value of the midpoint of the lane
        middle_y = int((left_lane[1][int(left_lane.shape[1]/2)] + right_lane[1][int(right_lane.shape[1]/2)])/2)

        # finding the corresponding indicies to the points in each lane closest to the middle_y value
        left_idx = (np.abs(left_lane[1] - middle_y)).argmin()
        right_idx = (np.abs(right_lane[1] - middle_y)).argmin()

        # finding the x value of the midpoint of the lane
        middle_x = int((left_lane[0][left_idx] + right_lane[0][right_idx])/2)

        # creating homogenous coordinates for the middle of the lane
        mid_pt_lane = (middle_x, middle_y, 1)

        # finding the error term
        e_p2p = mid_pt_lane[0] - width/2

        # drawing midpoint of lane onto output image
        cv2.circle(output_img, (middle_x, middle_y), 5, (0, 0, 255), 3)

        # drawing midpoint of vehicle path (taken as the middle of the screen)
        cv2.circle(output_img, (int(width/2), middle_y), 5, (0, 255, 0), 3)

        # drawing an arrow showing the error between the two points
        cv2.arrowedLine(output_img, (int(width/2), middle_y), (middle_x, middle_y), (255, 0, 0), 4)
        
        return e_p2p, output_img
    
    def point2line(self, left_lane, right_lane, width, output_img):
        # finds the point to line visual task specification

        # finding y value of the midpoint of the lane
        middle_y = int((left_lane[1][int(left_lane.shape[1]/2)] + right_lane[1][int(right_lane.shape[1]/2)])/2)

        # finding the corresponding indicies to the points in each lane closest to the middle_y value
        left_idx = (np.abs(left_lane[1] - middle_y)).argmin()
        right_idx = (np.abs(right_lane[1] - middle_y)).argmin()

        # finding the x value of the midpoint of the lane
        middle_x = int((left_lane[0][left_idx] + right_lane[0][right_idx])/2)

        # creating homogenous coordinates for the middle of the lane
        mid_pt_lane = (middle_x, middle_y, 1)

        # creating homogenous coordinates for the line of the vehicle path
        line_mid = np.cross((width/2, 500, 1), (width/2, 0, 1))

        # finding the error term
        e_p2l = (np.dot(mid_pt_lane, line_mid))/1000

        # drawing midpoint of lane onto output image
        cv2.circle(output_img, (middle_x, middle_y), 5, (0, 0, 255), 3)

        # drawing line of vehicle path (taken as the middle of the screen)
        cv2.line(output_img, (int(width/2), 550), (int(width/2), 400), (0, 255, 0), 4)

        # drawing an arrow showing the error between the vehicle path line and the midpoint of the lane
        cv2.arrowedLine(output_img, (int(width/2), middle_y), (middle_x, middle_y), (255, 0, 0), 4)

        return e_p2l, output_img
    
    def cent2point(self, left_lane, right_lane, width, output_img):
        # finds the point to point visual task specification but uses the centroid rather than the midpoint of the lane

        # finding the centroid of the lane polygon
        cent = self.get_centroid(left_lane, right_lane)

        # finding the error term
        e_p2p = cent[0] - width/2

        # drawing centroid of lane onto output image
        cv2.circle(output_img, (int(cent[0]), int(cent[1])), 5, (0, 0, 255), 3)

        # drawing midpoint of vehicle path (taken as the middle of the screen)
        cv2.circle(output_img, (int(width/2), int(cent[1])), 5, (0, 255, 0), 3)

        # drawing an arrow showing the error between the two points
        cv2.arrowedLine(output_img, (int(width/2), int(cent[1])), (int(cent[0]), int(cent[1])), (255, 0, 0), 4)

        return e_p2p, output_img
        
    def cent2line(self, left_lane, right_lane, width, output_img):
        # finds the point to line visual task specification but uses the centroid rather than the midpoint of the lane

        # finding the centroid of the lane polygon
        cent = self.get_centroid(left_lane, right_lane)

        # converting to homogenous coordinates
        cent_h = (cent[0], cent[1], 1)

        # finding the vehicle path line
        line_mid = np.cross((width/2, 500, 1), (width/2, 0, 1))

        # finding the error term
        e_p2l = (np.dot(cent_h, line_mid))/1000

        # drawing centroid of lane onto output image
        cv2.circle(output_img, (int(cent[0]), int(cent[1])), 5, (0, 0, 255), 3)

        # drawing midpoint of vehicle path (taken as the middle of the screen)
        cv2.line(output_img, (int(width/2), 550), (int(width/2), 400), (0, 255, 0), 4)

        # drawing an arrow showing the error between the vehicle path line and the centroid of the lane
        cv2.arrowedLine(output_img, (int(width/2), int(cent[1])), (int(cent[0]), int(cent[1])), (255, 0, 0), 4)

        return e_p2l, output_img

    def parlines(self, left_lane, right_lane, width, output_img):
        # finds the parallel lines task specification

        # finding the start and end of the lane
        lane_end = (int((left_lane[0][-1] + right_lane[0][-1])/2), left_lane[1][-1], 1)
        lane_start = (int((left_lane[0][0] + right_lane[0][0])/2), left_lane[1][0], 1)

        # finding the start and end of the midline
        midline_end = (width/2, left_lane[1][-1], 1)
        midline_start = (width/2, left_lane[1][0], 1)

        # finding the midline and lane in homogeneous coordinates
        midline = np.cross(midline_end, midline_start)
        lane = np.cross(lane_end, lane_start)

        # finding the error term
        e_pl_v = np.cross(midline, lane)
        e_pl = (np.sign(e_pl_v[1])*np.linalg.norm(e_pl_v))/1000000

        # drawing the two lines
        cv2.arrowedLine(output_img, (int(lane_start[0]), int(lane_start[1])), (int(lane_end[0]), int(lane_end[1])), (0, 0, 255), 4)
        cv2.arrowedLine(output_img, (int(midline_start[0]), int(midline_start[1])), (int(midline_end[0]), int(midline_end[1])), (0, 255, 0), 4)

        return e_pl, output_img
    
    def line2line(self, left_lane, right_lane, width, output_img):
        # finds the parallel lines task specification

        # finding the start and end of the lane
        lane_end = ((int((left_lane[0][-1] + right_lane[0][-1])/2)), left_lane[1][-1], 1)
        lane_start = ((int((left_lane[0][1] + right_lane[0][1])/2)), left_lane[1][0], 1)

        # finding the start and end of the midline
        middle_end = (width/2, left_lane[1][-1], 1)
        middle_start = (width/2, left_lane[1][0], 1)

        # finding the lane in homogeneous coordinates
        lane = np.cross(lane_end, lane_start)

        # finding the error term
        e_l2l = (np.dot(middle_end, lane) + np.dot(middle_start, lane))/1000

        # drawing the two lines
        cv2.arrowedLine(output_img, (int(lane_start[0]), int(lane_start[1])), (int(lane_end[0]), int(lane_end[1])), (0, 0, 255), 4)
        cv2.arrowedLine(output_img, (int(middle_start[0]), int(middle_start[1])), (int(middle_end[0]), int(middle_end[1])), (0, 255, 0), 4)

        return e_l2l, output_img
