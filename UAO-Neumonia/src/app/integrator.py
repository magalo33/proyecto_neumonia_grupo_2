# Módulo integrador que se encarga de orquestar las funciones de lectura de imagen,
import os
import cv2
import numpy as np

from read_img import read_dicom_file, read_jpg_file
from prediction import predict

def prediction(array):
    """
    Make a prediction based on the input array.

    Args:
        array (list or numpy.ndarray): The input data for making the prediction.

    Returns:
        The prediction result from the model.
    """
    return predict(array)

def read_dicom(path):
    """
    Reads a DICOM file from the specified path.

    Args:
        path (str): The file path to the DICOM file.

    Returns:
        DICOM object: The DICOM file read from the specified path.
    """
    return read_dicom_file(path)

def read_jpg(path):
    """
    Reads a JPG file from the specified path.

    Args:
        path (str): The file path to the JPG image.

    Returns:
        Image: The image object read from the file.
    """
    return read_jpg_file(path)

