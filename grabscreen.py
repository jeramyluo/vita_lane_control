'''
  File name: grabscreen.py
  Author(s):  Jeramy Luo - process_input() - small function to process input wrote by Jeramy
              Daniel Kukiela - grab_screen() - obtained online from https://github.com/Sentdex/pygta5/blob/master/original_project/grabscreen.py
  Purpose: Functions required to obtain and preprocess the input frame of the testing environment.
'''

import cv2
import numpy as np
import win32gui, win32ui, win32con, win32api

def process_input():
  # grabbing input screenshot from top left corner of screen
  input = grab_screen(region=(0,26,799,625))

  # converting to RGB colour
  input_rgb = cv2.cvtColor(input, cv2.COLOR_BGR2RGB)

  # creating border on screenshot to improve lane detection performance
  input_rgb_border = cv2.copyMakeBorder(input_rgb, 0, 0, 400, 400, borderType=cv2.BORDER_CONSTANT)

  return input_rgb_border

def grab_screen(region=None):

    hwin = win32gui.GetDesktopWindow()

    if region:
            left,top,x2,y2 = region
            width = x2 - left + 1
            height = y2 - top + 1
    else:
        width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
        height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
        left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
        top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)

    hwindc = win32gui.GetWindowDC(hwin)
    srcdc = win32ui.CreateDCFromHandle(hwindc)
    memdc = srcdc.CreateCompatibleDC()
    bmp = win32ui.CreateBitmap()
    bmp.CreateCompatibleBitmap(srcdc, width, height)
    memdc.SelectObject(bmp)
    memdc.BitBlt((0, 0), (width, height), srcdc, (left, top), win32con.SRCCOPY)
    
    signedIntsArray = bmp.GetBitmapBits(True)
    img = np.fromstring(signedIntsArray, dtype='uint8')
    img.shape = (height,width,4)

    srcdc.DeleteDC()
    memdc.DeleteDC()
    win32gui.ReleaseDC(hwin, hwindc)
    win32gui.DeleteObject(bmp.GetHandle())

    return cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)