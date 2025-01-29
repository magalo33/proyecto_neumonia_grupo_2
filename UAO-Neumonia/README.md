## Hola! Bienvenido a la herramienta para la detección rápida de neumonía

Deep Learning aplicado en el procesamiento de imágenes radiográficas de tórax en formato DICOM con el fin de clasificarlas en 3 categorías diferentes:

1. Neumonía Bacteriana

2. Neumonía Viral

3. Sin Neumonía

Aplicación de una técnica de explicación llamada Grad-CAM para resaltar con un mapa de calor las regiones relevantes de la imagen de entrada.

---

## Uso de la herramienta:

A continuación le explicaremos cómo empezar a utilizarla.

Requerimientos necesarios para el funcionamiento:

- Instale Docker
  https://www.docker.com/products/docker-desktop/

  La imagen creada mediante el Dockerfile ya contiene  la versión de python nesesaria(3.8) y el archivo requirements
  contiene las librerias nesesarias para la ejecución del proyecto.

- Instalar el plugin Dev Containers    
- Ejecute el proyecto en docker
  Teclee las teclas Control + Shift + P
  Seleccione la opción >Dev Containers: Reopen in Container

-  Uso de la Interfaz Gráfica:
  Una vez iniciado el contenedor de docker, ejecute el archivo main.py

## Arquitectura de archivos.

## main.py

Contiene el diseño de la interfaz gráfica utilizando Tkinter.

Los botones llaman métodos contenidos en otros scripts.

## integrator.py

Es un módulo que integra los demás scripts y retorna solamente lo necesario para ser visualizado en la interfaz gráfica.
Retorna la clase, la probabilidad y una imagen el mapa de calor generado por Grad-CAM.

## read_img.py

Script que lee la imagen en formato DICOM para visualizarla en la interfaz gráfica. Además, la convierte a arreglo para su preprocesamiento.

## preprocess_img.py

Script que recibe el arreglo proveniento de read_img.py, realiza las siguientes modificaciones:

## prediction.py

  Script que contiene el método que ejecuta la predicción del modelo.

## load_model.py

Script que lee el archivo binario del modelo de red neuronal convolucional previamente entrenado llamado 'WilhemNet86.h5'.

## grad_cam.py

Script que recibe la imagen y la procesa, carga el modelo, obtiene la predicción y la capa convolucional de interés para obtener las características relevantes de la imagen.

---

## Acerca del Modelo

La red neuronal convolucional implementada (CNN) es basada en el modelo implementado por F. Pasa, V.Golkov, F. Pfeifer, D. Cremers & D. Pfeifer
en su artículo Efcient Deep Network Architectures for Fast Chest X-Ray Tuberculosis Screening and Visualization.

Está compuesta por 5 bloques convolucionales, cada uno contiene 3 convoluciones; dos secuenciales y una conexión 'skip' que evita el desvanecimiento del gradiente a medida que se avanza en profundidad.
Con 16, 32, 48, 64 y 80 filtros de 3x3 para cada bloque respectivamente.

Después de cada bloque convolucional se encuentra una capa de max pooling y después de la última una capa de Average Pooling seguida por tres capas fully-connected (Dense) de 1024, 1024 y 3 neuronas respectivamente.

Para regularizar el modelo utilizamos 3 capas de Dropout al 20%; dos en los bloques 4 y 5 conv y otra después de la 1ra capa Dense.

## Acerca de Grad-CAM

Es una técnica utilizada para resaltar las regiones de una imagen que son importantes para la clasificación. Un mapeo de activaciones de clase para una categoría en particular indica las regiones de imagen relevantes utilizadas por la CNN para identificar esa categoría.

Grad-CAM realiza el cálculo del gradiente de la salida correspondiente a la clase a visualizar con respecto a las neuronas de una cierta capa de la CNN. Esto permite tener información de la importancia de cada neurona en el proceso de decisión de esa clase en particular. Una vez obtenidos estos pesos, se realiza una combinación lineal entre el mapa de activaciones de la capa y los pesos, de esta manera, se captura la importancia del mapa de activaciones para la clase en particular y se ve reflejado en la imagen de entrada como un mapa de calor con intensidades más altas en aquellas regiones relevantes para la red con las que clasificó la imagen en cierta categoría.

## Proyecto original por:



    • Sandra Luengas Aponte-ID UAO:2248280.
    • John Alexander Léon Torres-ID UAO: 2248372.
    • Jorge Leonardo Prada Dániel-ID UAO:2246604.
    • Miguel Arcesio Londoño Garzon-ID UAO: 2246382.


## Licencia

Este proyecto está bajo la **Licencia MIT**. Consulta https://opensource.org/licenses/MIT para más detalles.

### Resumen de la Licencia MIT

La Licencia MIT es una licencia permisiva que permite a cualquier persona usar, copiar, modificar y distribuir el software, incluso con fines comerciales, siempre que se incluya el aviso de copyright y la renuncia de responsabilidad en todas las copias o partes sustanciales del software.

Este software se distribuye "tal cual", sin ninguna garantía expresa o implícita.


## Notas de uso 
  Al generar el documento pdf usando Docker, este se guardará dentro del contenedor, por lo cual
  debe copiarlo desde el contenedor de docker y pegarlo en la ruta de su elección usando la siguiente instrucción:

  docker cp nombre_del_contenedor:/ruta/en/donde/guardo/archivo.pdf ~/ruta/de/destino/en/maquina/huesped/
