import numpy as np
import dlib
import cv2

def initiate_tracker(frame,id,bounding_boxes):
    trackeri = dlib.correlation_tracker()
    x,y,w,h = bounding_boxes[id]
    xmin = x
    ymin = y
    xmax = xmin+w
    ymax = ymin+h
    dlib_rect=dlib.rectangle(xmin,ymin,xmax,ymax)
    trackeri.start_track(frame,dlib_rect)
    return trackeri

def track_objects(trackers,frame,num_objects):
    boxes = []
    for i in range(len(trackers)):
        tracker[i].update(frame)
        track_rect = tracker[i].get_position()
        xmin  = int(track_rect.left())
        ymin  = int(track_rect.top())
        xmax = int(track_rect.right())
        ymax = int(track_rect.bottom())
        box = (xmin,ymin,xmax,ymax)
        boxes.append(box)
    return boxes
