# Módulo integrador que se encarga de orquestar las funciones de lectura de imagen,
import os
import cv2
import numpy as np

from read_img import read_dicom_file, read_jpg_file
from prediction import predict

def prediction(array):
    return predict(array)

def read_dicom(path):
    return read_dicom_file(path)

def read_jpg(path):
    return read_jpg_file(path)

