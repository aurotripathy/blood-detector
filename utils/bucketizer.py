#! /usr/bin/env python

import cv2
import numpy as np
from pudb import set_trace
import itertools

drawing = False # true if mouse is pressed
mode = True # if True, draw rectangle. Press 'm' to toggle to curve
ix,iy = -1,-1
yes_high = False
no_high = False

def pick_user_input(event, x, y, flags, param):
    global ix, iy, drawing, mode, yes_high, no_high, p

    if event == cv2.EVENT_LBUTTONDOWN:
        if yes_high:
            de_highlight_yes_box()
            yes_high = False
        if no_high:
            de_highlight_no_box()
            no_high = False
        if is_clicked_yes_box(x, y):
            highlight_yes_box()
            yes_high = True
        if  is_clicked_no_box(x, y):
            highlight_no_box()
            no_high = True
        if is_clicked_prev_box(x,y):
            print "Clicked prev button"
            get_prev_image()
        if is_clicked_next_box(x,y):
            print "Clicked next button"
            get_next_image()
            

def is_clicked_no_box(x, y):
    if  ((h - button_len - border) <= x <= (h - border)) and ((border) <= y <=  (button_len + border)):
        return True
    else:
        return False

def is_clicked_yes_box(x, y):
    if  ((border) <= x <= (border + button_len)) and ((border) <= x <= (border + button_len)):
        return True
    else:
        return False

def is_clicked_prev_box(x,y):
    if point_inside_polygon(x,y, p):
        return True
    else:
        return False

def is_clicked_next_box(x,y):
    if point_inside_polygon(x,y, n):
        return True
    else:
        return False

def highlight_no_box():
    cv2.rectangle(overlay, (h - button_len - border, border), (h - border , button_len + border), black, button_bw) 
    cv2.addWeighted(overlay, alpha, output, 1 - alpha, 0, output)


def highlight_yes_box():
    cv2.rectangle(overlay, (border,border), (border + button_len, border + button_len), black, button_bw)
    cv2.addWeighted(overlay, alpha, output, 1 - alpha, 0, output)


def de_highlight_yes_box():
    cv2.rectangle(overlay, (border,border), (border + button_len, border + button_len), white, button_bw)
    cv2.addWeighted(overlay, alpha, output, 1 - alpha, 0, output)


def de_highlight_no_box():
    cv2.rectangle(overlay, (h - button_len - border, border), (h - border , button_len + border), white, button_bw) 
    cv2.addWeighted(overlay, alpha, output, 1 - alpha, 0, output)


def draw_triangle(img, p1, p2, p3):
    pts = np.array([p1, p2, p3], np.int32)
    pts = pts.reshape((-1,1,2))
    cv2.polylines(img,[pts], True, (0, 0, 0), 2)

def midpoint(a, b):
    return((a[0] + b[0])/2, (a[1] + b[1])/2) 


def draw_next_prev():
    p_00 = [h - button_len - border, w - button_len - border]
    p_01 = [h - border             , w - button_len - border]
    p_10 = [h - button_len - border, w - border             ]
    p_11 = [h - border             , w - border             ]

    tp1 = midpoint(p_00, p_01)
    tp2 = midpoint(p_00, p_10)
    tp3 = midpoint(p_10, p_11)
    tp4 = midpoint(p_01, p_11)

    draw_triangle(overlay, tp1, tp2, tp3)
    draw_triangle(overlay, tp1, tp4, tp3)
    tri_prev = np.array([tp1, tp2, tp3], np.int32)
    tri_next = np.array([tp1, tp4, tp3], np.int32)
    return tri_next, tri_prev
                            

# determine if a point is inside a given polygon or not
# Polygon is a list of (x,y) pairs.
def point_inside_polygon(x,y,poly):

    n = len(poly)
    inside =False

    p1x,p1y = poly[0]
    for i in range(n+1):
        p2x,p2y = poly[i % n]
        if y > min(p1y,p2y):
            if y <= max(p1y,p2y):
                if x <= max(p1x,p2x):
                    if p1y != p2y:
                        xinters = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x,p1y = p2x,p2y

    return inside

def get_prev_image():
    pass


def get_next_image():
    pass

# set_trace()

img_list = ['/home/tempuser/Pictures/Lenna.jpg',
            '/home/tempuser/Pictures/Lenna.jpg',
            '/home/tempuser/Pictures/Lenna.jpg',
            '/home/tempuser/Pictures/Lenna.jpg',
            '/home/tempuser/Pictures/Lenna.jpg']
button_len = 50
white = (255, 255, 255)
green = (0, 255, 0)
red = (0,0,255)
black = (0,0,0)
border =  10
button_bw = 3
window_str = 'image'
for image in img_list:
    img = cv2.imread(image)
    h, w, c = img.shape
    overlay = img.copy()
    output = img.copy()
    cv2.rectangle(overlay, (border,border), (border + button_len, border + button_len), green, cv2.FILLED) 
    cv2.rectangle(overlay, (h - button_len - border, border), (h - border , button_len + border), red, cv2.FILLED) 


    n, p = draw_next_prev()
    print n, p
    # apply the overlay
    alpha = 0.3
    cv2.addWeighted(overlay, alpha, output, 1 - alpha, 0, output)
    
    cv2.namedWindow(window_str)
    cv2.setMouseCallback(window_str, pick_user_input)

    while(1):
        cv2.imshow(window_str, output)
        k = cv2.waitKey(1) & 0xFF
        if k == ord('m'):
            mode = not mode
        elif k == 27:
            break

    cv2.destroyAllWindows()
