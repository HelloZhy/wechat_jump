
import cv2
import numpy as np
import os,sys,time

pre = '/Users/zhy/Desktop/PythonProgram/opencv/jump/'
name = pre+'Screenshot_2018-01-05-13-36-21-302_com.tencent.mm.png'
# Screenshot_2018-01-05-13-33-00-455_com.tencent.mm.png
# Screenshot_2018-01-05-13-33-33-713_com.tencent.mm.png
# Screenshot_2018-01-05-13-34-24-792_com.tencent.mm.png
# Screenshot_2018-01-05-13-43-21-370_com.tencent.mm.png
# Screenshot_2018-01-05-13-36-21-302_com.tencent.mm.png
def distance(img):
    template = cv2.imread('/Users/zhy/Desktop/PythonProgram/opencv/jump/screencap/person.png')
    img = cv2.imread(img)
    # find person
    # img.shape => (row, col)
    # minPos (col, row)
    minVal, maxVal, minPos, maxPos = cv2.minMaxLoc(cv2.matchTemplate(img, template, 0))
    print('person:', minPos)
    cv2.rectangle(img, (minPos[0],minPos[1]),
                  (minPos[0]+template.shape[1], minPos[1]+template.shape[0]),
                  (255, 255, 255))

    # use canny to find top point
    roi = img[int(img.shape[0]/3):int(img.shape[0]*2/3), :]
    roi_canny = cv2.Canny(img, 100, 200)[int(img.shape[0]/3):int(img.shape[0]*2/3), :]

    # clear person
    # [row, col]
    _roi_person_loc = [minPos[1]-int(img.shape[0]/3), minPos[0]]
    edge_w = 3
    for row in range(_roi_person_loc[0]-edge_w, _roi_person_loc[0]+template.shape[0]+edge_w):
        for col in range(_roi_person_loc[1]-edge_w, _roi_person_loc[1]+template.shape[1]+edge_w):
            if col >= roi_canny.shape[1] or row >= roi_canny.shape[0]:
                pass
            else:
                roi_canny[row, col] = 0


    #[row, col]
    top_point = [-1, -1]
    if_find = False
    _counter = 0
    for row in range(roi_canny.shape[0]):
        for col in range(roi_canny.shape[1]):
            if roi_canny[row, col] == 255:
                if not if_find:
                    if_find = True
                    top_point[0] = row
                    top_point[1] = col
                else:
                    _counter+=1
        if if_find:
            break
    # _type True:rect False:circle
    _type = True
    print('next object:', top_point)
    if _counter > 4:
        _type = False
        print('object type: circle')
    else:
        print('object type: rect')

    cv2.circle(roi_canny, \
               (_roi_person_loc[1]+int(template.shape[1]/2),\
                _roi_person_loc[0]+template.shape[0]), 5, (255))

    if _type:
        p1 = [top_point[1], top_point[0]+60]
        cv2.circle(roi_canny, (top_point[1], top_point[0]+50), 5, (255))
    else:
        p1 = [top_point[1], top_point[0]+20]
        cv2.circle(roi_canny, (top_point[1], top_point[0]+20), 5, (255))
    p2 = [_roi_person_loc[1]+int(template.shape[1]/2),
          _roi_person_loc[0]+template.shape[0]]
    cv2.imshow('window', roi_canny)
    cv2.waitKey(30)
    #cv2.destroyAllWindows()

    return float(((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)**(1/2))

def capture():
    cmd = '/Users/zhy/AndroidEnvironmet/platform-tools/adb '
    os.system(cmd+'shell screencap /sdcard/cap.png')
    os.system(cmd+'pull /sdcard/cap.png '+pre)

def push(time):
    cmd = '/Users/zhy/AndroidEnvironmet/platform-tools/adb'
    os.system('sudo '+cmd+' shell input swipe 320 410 320 410 '+str(int(time)))

def main():
    name = pre+'cap.png'
    alpha = 1.355
    cv2.namedWindow('window')
    while True:
        capture()
        push(distance(name)*alpha)
        time.sleep(3)

if __name__ == '__main__':
    main()
