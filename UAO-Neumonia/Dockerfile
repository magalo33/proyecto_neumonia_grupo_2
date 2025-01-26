FROM python:3.8-slim

# Instala dependencias del sistema en un solo RUN
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
        python3-opencv \
        libgl1-mesa-glx \
        python3-tk \
        scrot \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /home/src

# Copia tu código al contenedor
COPY . ./

# Instala dependencias de Python (en un solo RUN para optimizar capas)
RUN pip install --upgrade pip && \
    pip install --upgrade --no-cache-dir pydicom && \
    pip install --no-cache-dir -r requirements.txt

# (Opcional) Si tu contenedor necesita ejecutar algo en particular al arrancar:
# CMD ["python", "tu_script.py"]
