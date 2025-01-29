# Módulo encargado de cargar el modelo entrenado
import tensorflow as tf
from tensorflow.keras.models import load_model


"""
This module is responsible for loading the trained model.

Functions:
    get_model: Loads and returns a pre-trained model from a specified file.

Dependencies:
    tensorflow
    tensorflow.keras.models.load_model
"""
def get_model():
    # Carga un modelo ya entrenado
    model = load_model("Modelo de Neumonia .h5-20250126/conv_MLP_84.h5", 
                       compile=False)
    return model
