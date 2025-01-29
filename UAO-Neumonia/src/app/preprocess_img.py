# Módulo encragado de recibir el arreglo de imagen (en BGR) y transformarlo
import cv2
import numpy as np

def preprocess(array):
    """
    Preprocesses an input image array by resizing, converting to grayscale, 
    applying CLAHE (Contrast Limited Adaptive Histogram Equalization), 
    normalizing, and expanding dimensions.

    Parameters:
    array (numpy.ndarray): Input image array.

    Returns:
    numpy.ndarray: Preprocessed image array with shape (1, 512, 512, 1).
    """
    array = cv2.resize(array, (512, 512))
    array = cv2.cvtColor(array, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(4, 4))
    array = clahe.apply(array)
    array = array / 255
    array = np.expand_dims(array, axis=-1)
    array = np.expand_dims(array, axis=0)
    return array
