
# By Brendan Murphy, b-murphy.ca

import cv2
import math

def select_aoi_bbox(window_name, img, crosshairs=True, rect_thickness=2, rect_color=[0, 220, 0], crosshairs_thickness=1,
                    crosshairs_color=[0, 0, 190]):

    down = False
    end_aoi = False
    cancel = False
    p1x = None
    p1y = None
    p2x = None
    p2y = None
    cross_x = -1
    cross_y = -1

    def click_event(event, x, y, flags, param):
        nonlocal p1x
        nonlocal p1y
        nonlocal p2x
        nonlocal p2y
        nonlocal down
        nonlocal end_aoi
        nonlocal cancel
        nonlocal cross_x
        nonlocal cross_y

        if event == cv2.EVENT_RBUTTONDOWN:
            cancel = True

        if event == cv2.EVENT_LBUTTONDOWN:
            down = True
            p1x = x
            p1y = y
            p2x = x
            p2y = y

        if event == cv2.EVENT_MOUSEMOVE:  # Is current mouse location
            if x < 0:  # Stop from going negative
                x = 0
            if y < 0:  # minus border / plus border - cv2.copyMakeBorder  not using
                y = 0
            cross_x = x
            cross_y = y

            if down == True:
                if x > img.shape[1]:  # Stop from going over img size
                    x = img.shape[1]
                if y > img.shape[0]:
                    y = img.shape[0]
                p2x = x
                p2y = y

        if event == cv2.EVENT_LBUTTONUP:  # param prints None, flags 0
            if cancel != True:
                down = False
                end_aoi = True
            else:
                cancel = False

    while True:
        im = img.copy()

        if crosshairs == True:
            cv2.line(im, (0, cross_y), (im.shape[1], cross_y), crosshairs_color, crosshairs_thickness)
            cv2.line(im, (cross_x, 0), (cross_x, im.shape[0]), crosshairs_color, crosshairs_thickness)

        if down == True or end_aoi == True:
            cv2.rectangle(im, (p1x, p1y), (p2x, p2y), rect_color, rect_thickness)

        cv2.imshow(window_name, im)
        cv2.setMouseCallback(window_name, click_event)  # does not stop code, has to be after imshow

        if end_aoi == True:
            end_aoi = False
            break

        if cancel == True:
            p1x = None
            p1y = None
            p2x = None
            p2y = None
            down = False
            end_aoi = False

        # Undo operation starts
        if cv2.waitKey(1) & 0xFF == ord('z'):
            return False

    cv2.destroyAllWindows()

    if p1y != None:
        pminy = min(p1y, p2y)
        pmaxy = max(p1y, p2y)
        pminx = min(p1x, p2x)
        pmaxx = max(p1x, p2x)

        return [pminx, pminy, pmaxx, pmaxy]
    else:
        print("[WARNING] No aoi box returned")


# To show circle draw circle on center point, with math hypot / 2 for thickness
def select_circle_aoi(window_name, img, crosshairs=True, circle_thickness=2, circle_color=[0, 220, 0], crosshairs_thickness=1,
               crosshairs_color=[0, 0, 190]):
    '''
    returns 2 key points, in order selected, unlike select_aoi, which ment for bboxes always starting from top letf.
    draw line also?
    a circle and also be calc from 2 pts equally near center of object
    '''

    down = False
    end_aoi = False
    cancel = False
    p1x = None
    p1y = None
    p2x = None
    p2y = None
    cross_x = -1
    cross_y = -1

    def click_event(event, x, y, flags, param):
        nonlocal p1x
        nonlocal p1y
        nonlocal p2x
        nonlocal p2y
        nonlocal down
        nonlocal end_aoi
        nonlocal cancel
        nonlocal cross_x
        nonlocal cross_y

        if event == cv2.EVENT_RBUTTONDOWN:
            cancel = True

        if event == cv2.EVENT_LBUTTONDOWN:
            down = True
            p1x = x
            p1y = y
            p2x = x
            p2y = y

        if event == cv2.EVENT_MOUSEMOVE:  # Is current mouse location
            if x < 0:  # Stop from going negative
                x = 0
            if y < 0:  # minus border / plus border - cv2.copyMakeBorder  not using
                y = 0
            cross_x = x
            cross_y = y

            if down == True:
                if x > img.shape[1]:  # Stop from going over img size
                    x = img.shape[1]
                if y > img.shape[0]:
                    y = img.shape[0]
                p2x = x
                p2y = y

        if event == cv2.EVENT_LBUTTONUP:  # param prints None, flags 0
            if cancel != True:
                down = False
                end_aoi = True
            else:
                cancel = False

    while True:
        im = img.copy()

        if crosshairs == True:
            cv2.line(im, (0, cross_y), (im.shape[1], cross_y), crosshairs_color, crosshairs_thickness)
            cv2.line(im, (cross_x, 0), (cross_x, im.shape[0]), crosshairs_color, crosshairs_thickness)

        if down == True or end_aoi == True:
            hyp = math.hypot((p1x - p2x), (p1y - p2y))
            cv2.line(im, (p1x, p1y), (p2x, p2y), [0, 0, 170], 1)
            cv2.circle(im, (p1x, p1y), 2, circle_color, -1)
            cv2.circle(im, (p1x, p1y), int(hyp), circle_color, circle_thickness)

        cv2.imshow(window_name, im)
        cv2.setMouseCallback(window_name, click_event)  # does not stop code, has to be after imshow

        if end_aoi == True:
            end_aoi = False
            break

        if cancel == True:
            p1x = None
            p1y = None
            p2x = None
            p2y = None
            down = False
            end_aoi = False

        # Undo operation starts
        if cv2.waitKey(1) & 0xFF == ord('z'):
            return False

    cv2.destroyAllWindows()

    if p1y != None:
        return [p1x, p1y, p2x, p2y]
    else:
        print("[WARNING] No aoi box returned")


