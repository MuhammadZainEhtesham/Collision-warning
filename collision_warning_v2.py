import numpy as np
import os
import cv2
import time
import psutil
import tflite_runtime.interpreter as tflite
from tflite_runtime.interpreter import load_delegate
import database
import tf_object_detector
from tf_object_detector import load_interpreter,detect_objects
import dlib_tracker
from dlib_tracker import initiate_tracker,track_objects
import collision_warning_API
from collision_warning_API import create_rec,update_frame_details,time_to_collision_RTD,time_to_collision_FRD,detect_crash

def fps(inference_time,video):
    try:
        fps = 1/inference_time
        return fps
    except:
        fps = video.get(cv2.CAP_PROP_FPS)
        return fps

liscence_plate ="XYZ-789"
resW = 300
resH = 300
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PRP_FOURCC,cv2.VideoWriter_fourcc('M','J','P','G'))
ret,frame = cap.read()
z = 1
frame = cv2.resize(frame,(resW,resH))
cv2.imshow('frame',frame)
LABELS_PATH = "labels.txt"
path_to_model = 'model4_edgetpu.tflite'
interpreter,input_details,output_details = load_interpreter(path_to_model)
bounding_boxes,objects,scores =  detect_objects(LABELS_PATH,interpreter,input_details,output_details,frame,0.47,resW,resH)
num_objects = len(objects)
frame_dict = create_rec(num_objects)
trackers = []
for id in range(num_objects):
    x,y,w,h = bounding_boxes[id]
    update_frame_details(frame_dict,w,id,resW)
    trackeri = initiate_tracker(frame,id,bounding_boxes)
    trackers.append(trackeri)
beep_frame = []
collision_points = [0]
while True:
    inference_start = time.time()
    ret,frame = cap.read()
    frame = cv2.resize(frame,(resW,resH))
    if z % 30 == 0:
        bounding_boxes,objects,scores = dlib_object_tracking.detect_objects(LABELS_PATH,interpreter,input_details,output_details,frame,0.47,300,300)
        num_objects = len(objects)
        frame_dict = create_rec(num_objects)
        trackers = []
        for id in range(num_objects):
            x,y,w,h = bounding_boxes[id]
            update_frame_details(frame_dict,w,id,resW)
            trackeri = initiate_tracker(frame,id,bounding_boxes)
            trackers.append(trackeri)
        boxes = track_objects(trackers,frame,num_objects)
    else:
        boxes = track_objects(trackers,frame,num_objects)
    for id in range(num_objects):
        xmin,ymin,xmax,ymax = boxes[id]
        update_frame_details(frame_dict,xmax-xmin,id,resW)
        ttc = time_to_collision_RTD(frame_dict,id)
        cv2.rectangle(frame,(xmin,ymin),(xmax,ymax),(0,0,255),2)
        cv2.putText(frame, str(ttc), (int(x + (w/2)), int(y + (h/2))), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        if ttc < 5 and ttc > 0:
            crash_code = detect_crash(z,id,frame_dict,beep_list,collision_points)
            if crash_code == 10:
                break
            else:
                continue
    inference_end = time.time()
    inference_time = inference_end - inference_start
    frameps = round(fps(inference_time,cap),2)
    cv2.putText(frame, str(frameps), (50, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    cv2.imshow('frame',frame)
    print(frameps)
    z+=1
    if cv2.waitKey(1) == ord('q'):
        break
database.update_properties(liscence_plate,100-sum(collision_points))
process = psutil.Process(os.getpid())
print('memory usage is',process.memory_info().rss)
