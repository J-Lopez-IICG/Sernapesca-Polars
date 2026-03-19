# 1. Imagen base
FROM python:3.11-slim

# 2. Entorno limpio
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Argumentos dinámicos (con 1000 por defecto) ---
ARG UID=1000
ARG GID=1000

# Creamos el grupo y usuario usando las variables dinámicas
RUN groupadd -g ${GID} kedro_group && \
    useradd -l -u ${UID} -g kedro_group -m -s /bin/bash kedro_user
# ----------------------------------------------------------

# 3. PRIMERO copiamos e instalamos dependencias
# Hacemos esto antes de copiar todo el código para aprovechar el "caché" de Docker
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. DESPUÉS copiamos el resto del proyecto
COPY . .

# Cambiamos el propietario de la carpeta al nuevo usuario
RUN chown -R kedro_user:kedro_group /app

# Instruimos a Docker para que cambie a este usuario ---
USER kedro_user

# 5. El comando por defecto
CMD ["kedro", "run"]