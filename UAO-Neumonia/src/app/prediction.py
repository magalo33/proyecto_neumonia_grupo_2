# Módulo prediction que se encarga de ejecutar la predicción del modelo
import numpy as np

from grad_cam import grad_cam
from load_model import get_model
from preprocess_img import preprocess




def predict(array):
    """
    Predicts the class of a given image array and generates a Grad-CAM heatmap.

    Args:
        array (numpy.ndarray): The input image array to be predicted.

    Returns:
        tuple: A tuple containing:
            - label (str): The predicted class label ('bacteriana', 'normal', 'viral').
            - proba (float): The probability of the predicted class in percentage.
            - heatmap (numpy.ndarray): The Grad-CAM heatmap superimposed on the input image.
    """
    #   1. call function to pre-process image: it returns image in batch format
    batch_array_img = preprocess(array)
    #   2. call function to load model and predict: it returns predicted class
    #  and probability
    model = get_model()
    # model_cnn = tf.keras.models.load_model('conv_MLP_84.h5')
    prediction = np.argmax(model.predict(batch_array_img))
    proba = np.max(model.predict(batch_array_img)) * 100
    label = ""
    if prediction == 0:
        label = "bacteriana"
    if prediction == 1:
        label = "normal"
    if prediction == 2:
        label = "viral"
    #   3. call function to generate Grad-CAM: it returns an image with a 
    # superimposed heatmap
    heatmap = grad_cam(array)
    return (label, proba, heatmap)


