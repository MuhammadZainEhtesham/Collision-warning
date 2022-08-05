import numpy as np
import cv2
import os


def load_labels(filename):
  with open(filename, 'r') as f:
    return [line.strip() for line in f.readlines()]

def load_interpreter(path_to_model):
    interpreter = tflite.Interpreter(model_path = path_to_model,experimental_delegates=[load_delegate('libedgetpu.so.1')])
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    return interpreter,input_details,output_details

def detect_objects(LABELS_PATH,interpreter,input_details,output_details,frame,min_threshold,resW,resH):#returns bounding box coordinates of the detected objects in a list
    bounding_boxes = []
    objects = []
    prediction_score = []
    min_config_threshhold = min_threshold
    imW, imH = int(resW), int(resH)
    labels = load_labels(LABELS_PATH)
    # interpreter = interpreter
    #  #get model details
    # input_details = input_details
    # output_details = output_details
    height = input_details[0]['shape'][1]
    width = input_details[0]['shape'][2]
    #check the type of input tensor
    floating_model = (input_details[0]['dtype'] == np.float32)

    input_mean = 127.5
    input_std = 127.5
    frame_resized = cv2.resize(frame, (width, height))
    input_data = np.expand_dims(frame_resized, axis=0)
    if floating_model:
        input_data = (np.float32(input_data) - input_mean) / input_std
    interpreter.set_tensor(input_details[0]['index'],input_data)
    interpreter.invoke()
    # Retrieve detection results
    boxes = interpreter.get_tensor(output_details[0]['index'])[0] # Bounding box coordinates of detected objects
    classes = interpreter.get_tensor(output_details[1]['index'])[0] # Class index of detected objects
    scores = interpreter.get_tensor(output_details[2]['index'])[0] # Confidence of detected objects
    for i in range(len(scores)):
        if ((scores[i] > min_config_threshhold) and (scores[i] <= 1.0)):
            if classes[i] == 2:
                mid_x = (boxes[i][3] + boxes[i][1]) / 2
                mid_y = (boxes[i][2] + boxes[i][0]) / 2
                if mid_x >0.3 and mid_x <0.7 and (boxes[i][3] - boxes[i][1]) > 0.2:
                    ymin = int(max(1,(boxes[i][0] * imH)))
                    xmin = int(max(1,(boxes[i][1] * imW)))
                    ymax = int(min(imH,(boxes[i][2] * imH)))
                    xmax = int(min(imW,(boxes[i][3] * imW)))
                    object_name = labels[int(classes[i])] # Look up object name from "labels" array using class index
                    score = int(scores[i]*100)
                    bb = xmin,ymin,xmax-xmin,ymax-ymin
                    bounding_boxes.append(tuple(bb))
                    objects.append(object_name)
                    prediction_score.append(score)
    return bounding_boxes,objects,scores
