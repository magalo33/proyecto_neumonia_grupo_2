FROM python:3.8-slim

# Instalar dependencias
RUN apt-get update -y && \
    apt-get install -y --no-install-recommends \
        python3-opencv \
        libgl1-mesa-glx \
        python3-tk \
        scrot \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /home/src

# Crea y activa el entorno virtual
RUN python -m venv venv


# Copia tu código al contenedor
COPY . ./

# Instalar dependencias de Python (en un solo RUN para optimizar capas)
RUN pip install --upgrade pip && \
    pip install --upgrade --no-cache-dir pydicom && \
    pip install --no-cache-dir -r requirements.txt

