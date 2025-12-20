FROM python:3.11-slim

# Evita buffers en logs
ENV PYTHONUNBUFFERED=1

# Crea directorio de trabajo
WORKDIR /app

# Instala dependencias del sistema si hace falta (comentado por defecto)
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     curl && rm -rf /var/lib/apt/lists/*

# Copia requirements e instala
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copia el código
COPY . /app

# Comando de arranque
CMD ["python", "main.py"]