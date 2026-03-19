# 1. Imagen base
FROM python:3.11-slim

# 2. Entorno limpio
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN groupadd -g 1000 kedro_group && \
    useradd -l -u 1000 -g kedro_group -m -s /bin/bash kedro_user

# 3. PRIMERO copiamos e instalamos dependencias
# Hacemos esto antes de copiar todo el código para aprovechar el "caché" de Docker
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. DESPUÉS copiamos el resto del proyecto
COPY . .

RUN chown -R kedro_user:kedro_group /app

# 5. El comando que mencionaste
CMD ["kedro", "run"]
