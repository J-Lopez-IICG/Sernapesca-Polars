# 1. Imagen base
FROM python:3.11-slim

# 2. Entorno limpio
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# 3. PRIMERO copiamos e instalamos dependencias
# Hacemos esto antes de copiar todo el código para aprovechar el "caché" de Docker
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. DESPUÉS copiamos el resto del proyecto
COPY . .

# 5. El comando que mencionaste
CMD ["kedro", "run"]