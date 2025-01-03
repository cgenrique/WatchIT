# Imagen base oficial de Python
FROM python:3.9-slim

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar los archivos necesarios al contenedor
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código de la aplicación
COPY src ./src
COPY ./src/data ./src/data

# Exponer el puerto en el que corre la aplicación
EXPOSE 5000

# Comando para ejecutar la aplicación
CMD ["python", "src/app.py"]

LABEL org.opencontainers.image.source="https://github.com/cgenrique/WatchIT"
LABEL org.opencontainers.image.description="WatchIT - Containerized movie management app"
LABEL org.opencontainers.image.licenses="MIT"

