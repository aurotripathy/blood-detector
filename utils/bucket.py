#! /usr/bin/env python

'''
Input file is a set of indexes
Output is two directories containing files separated by the choice 
we make via the UI.
'''

import cv2
import numpy as np
import time
import os
from pudb import set_trace
from argparse import ArgumentParser
import shutil
import keycode

def handle_mouse_activity(event, x, y, flags, params):
    global dst, is_yes_no_selection_made, copy_choice
    if event == cv2.EVENT_LBUTTONDOWN:
        if is_inside_no_box(x,y):
            print 'inside no box'
            select_no(auto_next)
        elif is_inside_yes_box(x,y):
            print 'inside yes box'
            select_yes(auto_next)
        elif is_inside_next_box(x, y):
            print 'inside next box'
            goto_next()
        elif is_inside_prev_box(x, y):
            print 'inside prev box'
            goto_prev()

    cv2.imshow(window_str, dst)

def handle_keystrokes():
    while (1):
        key = cv2.waitKey(0)
        if key in keycode.KEY_ESCAPE or key in keycode.KEY_CLOSE_WINDOW:
            break;
        elif  (key & 0xFF) in [ord("y"), ord("Y")] :
            print 'Yes'   
            select_yes(auto_next)
        elif  (key & 0xFF) in [ord("n"), ord("Y")] :
            print 'No'
            select_no(auto_next)
        elif key in keycode.KEY_RIGHT or key in keycode.KEY_SPACE:
            print 'Next'
            goto_next()
        elif key in keycode.KEY_LEFT:
            print 'Prev'
            goto_prev()
        else :
            print 'key {}'.format(key)

        cv2.imshow(window_str, dst)


def select_no(auto_next):
    global dst, is_yes_no_selection_made, copy_choice, uncopy_choice
    hightlight_no_box()
    de_hightlight_yes_box()
    dst = cv2.bitwise_or(img, ui)
    is_yes_no_selection_made = True
    copy_choice = 'no'
    uncopy_choice = 'yes'
    if auto_next == True :
        goto_next();

def select_yes(auto_next):
    global dst, is_yes_no_selection_made, copy_choice, uncopy_choice
    hightlight_yes_box()
    de_hightlight_no_box()
    dst = cv2.bitwise_or(img, ui)
    is_yes_no_selection_made = True
    copy_choice = 'yes'
    uncopy_choice = 'no'
    if auto_next == True :
        goto_next();

def goto_next():
    global dst, is_yes_no_selection_made, copy_choice, uncopy_choice
    if is_yes_no_selection_made:
        highlight_next_box(n)
        de_highlight_prev_box(p)
        dst = cv2.bitwise_or(img, ui)
        copy_current_image(copy_choice)
        uncopy_current_image(uncopy_choice)
        get_next_image()
        is_yes_no_selection_made = False
        prepare_load_image()

def goto_prev():
    global dst, is_yes_no_selection_made, copy_choice, uncopy_choice
    if is_yes_no_selection_made:
        highlight_prev_box(p)
        de_highlight_next_box(n)
        dst = cv2.bitwise_or(img, ui)
        copy_current_image(copy_choice)
        uncopy_current_image(uncopy_choice)
        get_prev_image()
        is_yes_no_selection_made = False
        prepare_load_image()


def copy_current_image(c):
    if c == 'no':
        shutil.copyfile(img_list[cursor], 
                        no_folder + os.path.basename(img_list[cursor]))
    elif c == 'yes':
        shutil.copyfile(img_list[cursor], 
                        yes_folder + os.path.basename(img_list[cursor]))
    else :
        print 'Invalid Choice'

def uncopy_current_image(c):
    if c == 'no':
        if os.path.isfile(no_folder + os.path.basename(img_list[cursor])):
            os.remove(no_folder + os.path.basename(img_list[cursor]))
    elif c == 'yes':
        if os.path.isfile(yes_folder + os.path.basename(img_list[cursor])):
            os.remove(yes_folder + os.path.basename(img_list[cursor]))
    else :
        print 'Invalid Choice'

def is_yes_processed():
    if os.path.isfile(yes_folder + os.path.basename(img_list[cursor])):
        return True
    return False

def is_no_processed():
    if os.path.isfile(no_folder + os.path.basename(img_list[cursor])):
        return True
    return False

def is_inside_no_box(x, y):
    if  ((x_len - button_len - border) <= x <= (x_len - border)) and ((border) <= y <=  (button_len + border)):
        return True
    else:
        return False

def is_inside_yes_box(x, y):
    if  ((border) <= x <= (border + button_len)) and ((border) <= y <= (border + button_len)):
        return True
    else:
        return False

def hightlight_yes_box():
    ui[border:border+button_len, border:border + button_len, green_plane] = 255

def de_hightlight_yes_box():
    ui[border:border+button_len, border:border + button_len, green_plane] = 0

def hightlight_no_box():
    ui[border : border + button_len, x_len - button_len - border : x_len - border, red_plane] = 255

def de_hightlight_no_box():
    ui[border : border + button_len, x_len - button_len - border : x_len - border, red_plane] = 0

def draw_yes_box():
    cv2.rectangle(img, (border, border), (border + button_len, border + button_len), green, button_bw) 

def draw_no_box():
    cv2.rectangle(img, (x_len - button_len - border, border), (x_len - border , button_len + border), red, button_bw)     


#---triangle primitives---

def draw_triangle_outline(img, pts):
    pts = pts.reshape((-1,1,2))
    cv2.polylines(img, [pts], True, black, 2)

def midpoint(a, b):
    return((a[0] + b[0])/2, (a[1] + b[1])/2) 

def draw_next_prev_button(x_l, y_l):
    p_00 = [x_l - button_len - border, y_l - button_len - border]
    p_01 = [x_l - border             , y_l - button_len - border]
    p_10 = [x_l - button_len - border, y_l - border             ]
    p_11 = [x_l - border             , y_l - border             ]

    tp1 = midpoint(p_00, p_01)
    tp2 = midpoint(p_00, p_10)
    tp3 = midpoint(p_10, p_11)
    tp4 = midpoint(p_01, p_11)

    tri_prev = np.array([tp1, tp2, tp3], np.int32)
    tri_next = np.array([tp1, tp4, tp3], np.int32)
    draw_triangle_outline(img, tri_prev)
    draw_triangle_outline(img, tri_next)
    return tri_next, tri_prev
                            

# determine if a point is inside a given polygon or not
# Polygon is a list of (x,y) pairs.
def is_point_inside_polygon(x,y,poly):

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

def is_inside_next_box(x,y):
    if is_point_inside_polygon(x, y, n):
        return True
    else:
        return False

def is_inside_prev_box(x,y):
    if is_point_inside_polygon(x,y, p):
        return True
    else:
        return False

def highlight_prev_box(pts):
    pts = pts.reshape((-1,1,2))
    cv2.fillPoly(ui, [pts], l_black)

def de_highlight_prev_box(pts):
    pts = pts.reshape((-1,1,2))
    cv2.fillPoly(ui, [pts], black)


def highlight_next_box(pts):
    pts = pts.reshape((-1,1,2))
    cv2.fillPoly(ui, [pts], l_black)

def de_highlight_next_box(pts):
    pts = pts.reshape((-1,1,2))
    cv2.fillPoly(ui, [pts], black)


def get_prev_image():
    global cursor, img, roll_to_next
    if cursor > 0:
        cursor -= 1
        print "getting prev {}".format(img_list[cursor])
        roll_to_next = True


def get_next_image():
    global cursor, img, roll_to_next
    if cursor < len(img_list) -1:
        cursor += 1
        print "getting next {}".format(img_list[cursor])
        roll_to_next = True


def get_parameters():
    parser = ArgumentParser()
    parser.add_argument("-i", "--index-file", dest="index_file",
                         help="file with all the indexes", required=True)
    parser.add_argument("-q", "--question", dest="question",
                         help="Question that is shown on the image", required=True)
    parser.add_argument("-a", "--auto-load", dest="auto_load", 
                        help="Autoload till categorized images", 
                        action = "store_true",  required=False)
    parser.add_argument("-n", "--auto-next", dest="auto_next", 
                        help="Auto step to next images", 
                        action = "store_true",  required=False)
    args = parser.parse_args()
    return args.index_file, args.question, args.auto_load, args.auto_next


def get_image_list(f_name):
    with open(f_name, 'r') as f:
        return f.read().splitlines()

def write_on_screen(x, y, str):
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img, str,(x, y), font, 1, black, 1)


def set_default_choice():
    if copy_choice == 'no':
        hightlight_no_box()
        de_hightlight_yes_box()

def prepare_load_image():
    global auto_load
    global img, dst, ui, n, p, x_len, y_len
    global copy_choice, uncopy_choice, is_yes_no_selection_made, roll_to_next

    copy_choice = None
    uncopy_choice = None
    roll_to_next = False
    is_yes_no_selection_made = False
    img = cv2.imread(img_list[cursor])
    y_len, x_len, c = img.shape
    print 'x {}, y {}'.format(x_len, y_len)
    ui = np.zeros((y_len, x_len, 3), np.uint8)

    draw_yes_box()
    draw_no_box()
    write_on_screen((x_len - 2 * border)/2 - 20 , border * 3, question_str)
    n, p = draw_next_prev_button(x_len, y_len)
    dst = cv2.add(img, ui)

    if (is_yes_processed() and not is_no_processed()):
        select_yes(auto_load)
    elif (is_no_processed() and not is_yes_processed()):
        select_no(auto_load)

        auto_load = False

index_file, question_str, auto_load, auto_next = get_parameters()
img_list = get_image_list(index_file)

for img_url in img_list:
    print img_url

if auto_load == True:
    print "Auto loading Till classified images."
if auto_next == True:
    print "Auto progress without NEXT"

yes_folder = 'yes_blood/'
no_folder  = 'no_blood/'

if not os.path.isdir(yes_folder):
    os.mkdir (yes_folder)
if not os.path.isdir(no_folder):
    os.mkdir (no_folder)

cursor = 0

border =  10
button_bw = 2
button_len = 50
green = (0, 255, 0)
red = (0, 0, 255)
black = (0, 0, 0)
l_black = (128, 128, 128)
green_plane = 1
red_plane = 2

window_str = question_str
prepare_load_image()

cv2.namedWindow(window_str,cv2.WINDOW_NORMAL)
cv2.moveWindow(window_str, 0,0)

cv2.imshow(window_str, dst)

cv2.setMouseCallback(window_str, handle_mouse_activity)
handle_keystrokes()

cv2.destroyAllWindows()

# references
# http://www.ariel.com.au/a/python-point-int-poly.html
