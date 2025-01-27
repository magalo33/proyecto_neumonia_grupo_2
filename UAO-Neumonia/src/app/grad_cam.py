# Módulo encargado de generar Grad-CAM y superponerlo en la imagen original
import numpy as np
import cv2
import tensorflow as tf
import tensorflow.keras.backend as K

from load_model import get_model
from preprocess_img import preprocess

def grad_cam(array):
    """
    Genera un Grad-CAM para resaltar las áreas importantes de una imagen de entrada.

    Args:
        array (numpy.ndarray): Imagen de entrada procesada como un array.
    
    Returns:
        numpy.ndarray: Imagen original con un mapa de calor superpuesto.
    """
    # Preprocesar la imagen
    img = preprocess(array)

    # Cargar el modelo
    model = get_model()

    # Obtener la capa convolucional final
    last_conv_layer = model.get_layer("conv10_thisone")

    # Crear un modelo intermedio para obtener características
    grad_model = Model(
        inputs=model.input,
        outputs=[last_conv_layer.output, model.output]
    )

    # Usar GradientTape para calcular los gradientes
    with tf.GradientTape() as tape:
        conv_outputs, predictions = grad_model(img)
        predicted_class = tf.argmax(predictions[0])
        loss = predictions[:, predicted_class]

    # Calcular gradientes de la pérdida con respecto a las salidas de la capa convolucional
    grads = tape.gradient(loss, conv_outputs)

    # Promediar los gradientes sobre los ejes espaciales
    pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))

    # Multiplicar cada canal por su gradiente promedio
    conv_outputs = conv_outputs[0].numpy()
    pooled_grads = pooled_grads.numpy()
    for i in range(pooled_grads.shape[-1]):
        conv_outputs[:, :, i] *= pooled_grads[i]

    # Crear el mapa de calor
    heatmap = np.mean(conv_outputs, axis=-1)
    heatmap = np.maximum(heatmap, 0)  # Aplicar ReLU
    heatmap /= np.max(heatmap)  # Normalizar entre 0 y 1
    heatmap = cv2.resize(heatmap, (array.shape[1], array.shape[0]))
    heatmap = np.uint8(255 * heatmap)
    heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)

    # Superponer el mapa de calor a la imagen original
    superimposed_img = cv2.addWeighted(array, 0.8, heatmap, 0.2, 0)
    return superimposed_img[:, :, ::-1]
