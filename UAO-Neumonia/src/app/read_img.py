# Módulo encargado de la lectura de las imágenes
import cv2
import numpy as np
import pydicom as dicom
from PIL import Image
import os

def read_dicom_file(path):
    """
    Reads a DICOM file from the specified path and returns the image in RGB format and the original image array.

    Args:
        path (str): The file path to the DICOM file.

    Returns:
        tuple: A tuple containing:
            - img_RGB (numpy.ndarray): The image in RGB format.
            - original_image (PIL.Image.Image): The original image array.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        Exception: If there is an error reading the DICOM file.
    """
    try:
        if not os.path.exists(path):
            raise FileNotFoundError(f"El archivo {path} no existe.")

        img = dicom.dcmread(path)
        img_array = img.pixel_array

        # Normalización a 0-255 solo si es necesario
        img2 = img_array.astype(float)
        if img2.max() > 0:
            img2 = (img2 - img2.min()) / (img2.max() - img2.min()) * 255.0
        img2 = np.uint8(img2)

        # Convertir a RGB
        img_RGB = cv2.cvtColor(img2, cv2.COLOR_GRAY2RGB)

        return img_RGB, Image.fromarray(img_array)

    except Exception as e:
        print(f"Error al leer el archivo DICOM: {e}")
        return None, None


def read_jpg_file(path):
    """
    Reads a JPG image file from the specified path, converts it to grayscale if necessary,
    normalizes the pixel values, and returns the processed image along with the original image.

    Args:
        path (str): The file path to the JPG image.

    Returns:
        tuple: A tuple containing:
            - img2 (numpy.ndarray): The processed grayscale image.
            - original_img (PIL.Image.Image): The original image.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        ValueError: If the image cannot be read or is invalid.
        Exception: For any other exceptions that occur during the process.
    """
    try:
        if not os.path.exists(path):
            raise FileNotFoundError(f"El archivo {path} no existe.")

        img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
        if img is None:
            raise ValueError(
                "No se pudo leer la imagen. Verifica que el archivo sea válido."
                )

        # Convertir a escala de grises si es necesario
        if len(img.shape) == 2:  # Imagen en escala de grises
            img2 = img
        else:
            img2 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Normalización solo si es necesario
        img2 = img2.astype(float)
        if img2.max() > 0:
            img2 = (img2 - img2.min()) / (img2.max() - img2.min()) * 255.0
        img2 = np.uint8(img2)

        return img2, Image.fromarray(img)

    except Exception as e:
        print(f"Error al leer el archivo de imagen: {e}")
        return None, None


def read_image_file(path):
    """
    Reads an image file from the given path and returns its content based on the file extension.
    Parameters:
    path (str): The file path to the image.
    Returns:
    tuple: A tuple containing the image data and metadata if the file is successfully read.
           Returns (None, None) if the file format is not supported.
    Supported formats:
    - DICOM: 'dcm', 'dicom'
    - Image: 'jpg', 'jpeg', 'png', 'bmp', 'tiff'
    Note:
    This function relies on `read_dicom_file` and `read_jpg_file` functions to read the respective file formats.
    """
    extension = path.lower().split('.')[-1]
    
    if extension in ['dcm', 'dicom']:
        return read_dicom_file(path)
    elif extension in ['jpg', 'jpeg', 'png', 'bmp', 'tiff']:
        return read_jpg_file(path)
    else:
        print(f"Formato no soportado: {extension}")
        return None, None
