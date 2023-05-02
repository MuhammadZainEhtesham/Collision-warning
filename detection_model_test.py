from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import numpy as np
import cv2
import os
import tflite_runtime.interpreter as tflite
import importlib.util
from threading import Thread
import sys


def load_interpreter(path_to_model):
    interpreter = tflite.Interpreter(model_path = path_to_model)
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    return interpreter,input_details,output_details


path_to_model = r'F:\DSML-projects\Unzila\scripts\model/wife.tflite'
interpreter,input_details,output_details = load_interpreter(path_to_model)
print(output_details)
