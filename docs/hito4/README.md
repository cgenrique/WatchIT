# 🍿 WatchIT 📽️ - Hito 4

En este hito, se ha diseñado e implementado un clúster de servicios utilizando Docker Compose para desplegar la aplicación WatchIT junto con un servicio de base de datos. Esto permite un despliegue reproducible y fácilmente escalable de la aplicación en cualquier entorno.

## 🚀 Objetivos

- Crear un contenedor para la aplicación desarrollado en hitos previos.
- Diseñar un clúster de servicios utilizando `docker-compose.yaml`, incluyendo:
  - Un contenedor para la aplicación WatchIT.
  - Un contenedor para la base de datos MongoDB.
  - Volúmenes para almacenamiento persistente de datos.
- Publicar la imagen del contenedor en GitHub Packages.
- Configurar pruebas automáticas para validar el clúster.
- Documentar toda la infraestructura y configuración.

## 🔨 Cambios realizados

### **1. Dockerfile**
- **Archivo:** `Dockerfile`
- **Descripción:** Define cómo se construye el contenedor de la aplicación WatchIT, incluyendo la instalación de dependencias necesarias.

```bash
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

```

### **2. Archivo docker-compose.yaml**
- **Archivo:** `docker-compose.yaml`
- **Descripción:** Orquesta la composición de contenedores, estableciendo la comunicación entre la aplicación y MongoDB, mapeo de puertos y definición de volúmenes.

```bash
version: "3.9"

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "5000:5000"
    volumes:
      - ./logs:/app/logs
      - ./data:/app/data
    environment:
      - FLASK_ENV=development
      - DOCKERIZED=true
    depends_on:
      - mongodb

  mongodb:
    image: mongo:latest
    container_name: mongodb
    ports:
      - "27017:27017"
    volumes:
      - mongodb_data:/data/db

  mongo-express:
    image: mongo-express:latest
    container_name: mongo-express
    restart: always
    ports:
      - "8081:8081"
    environment:
      - ME_CONFIG_MONGODB_SERVER=mongodb

volumes:
  mongodb_data:

```
### **3. Workflow de GitHub Actions**
- **Archivo:** `github-actions.yaml`
- **Descripción:** Automatiza la construcción y publicación de la imagen Docker, así como la ejecución de pruebas para validar el funcionamiento del clúster.
```bash
name: Run Tests and Push Docker Image

on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main

jobs:
  build-and-test:
    runs-on: ubuntu-latest

    steps:
      - name: Check out the code
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.x"

      - name: Install Docker and Docker Compose
        run: |
          sudo apt-get update
          sudo apt-get install -y \
            docker-ce docker-ce-cli containerd.io
          sudo curl -L "https://github.com/docker/compose/releases/download/$(curl -s https://api.github.com/repos/docker/compose/releases/latest | grep tag_name | cut -d '"' -f 4)/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
          sudo chmod +x /usr/local/bin/docker-compose
          docker-compose --version

      - name: Log in to GitHub Docker Registry
        env:
          CR_PAT: ${{ secrets.CR_PAT }}
        run: echo "${CR_PAT}" | docker login ghcr.io -u ${{ github.actor }} --password-stdin

      - name: Build Docker Image
        working-directory: .
        run: |
          docker build -t ghcr.io/${{ github.repository_owner }}/watchit:latest -f Dockerfile .

      - name: Push Docker Image to GitHub Packages
        run: docker push ghcr.io/${{ github.repository_owner }}/watchit:latest

      - name: Set up Docker Compose
        run: |
          docker compose up -d
          sleep 10

      - name: Install dependencies
        run: |
          python -m venv .venv
          source .venv/bin/activate
          pip install -r requirements.txt

      - name: Set environment variable for tests
        run: |
          echo "TEST_ENV=true" >> $GITHUB_ENV

      - name: Run tests
        run: |
          source .venv/bin/activate
          pytest tests/

      - name: Tear down Docker Compose
        if: always()
        run: docker compose down

```
## 📚 Documentación de la infraestructura

### **Clúster de contenedores**
El clúster incluye:
1. **Contenedor WatchIT (app-1)**: Contiene la lógica de la aplicación.
2. **Contenedor MongoDB (mongodb)**: Almacena los datos de las películas.
3. **Contenedor Mongo-Express (mongo-express)**: Interfaz web para administrar la base de datos MongoDB.
4. **Volumen**: Persistencia de datos de MongoDB.

### **Estructura del `docker-compose.yaml`**
- **Servicios:**
  - **`app-1`**: Contenedor que ejecuta la aplicación Flask.
  - **`mongodb`**: Contenedor que ejecuta la base de datos MongoDB.
  - **`mongo-express`**: Interfaz web para interactuar con MongoDB.

- **Puertos mapeados:**
  - **Aplicación WatchIT:** `5000:5000`
  - **MongoDB:** `27017:27017`
  - **Mongo-Express:** `8081:8081`

- **Volúmenes:**
  - **MongoDB Data:** Persistencia de datos entre reinicios del contenedor.

---

### **Explicación del Dockerfile**
El `Dockerfile` utiliza como base la imagen oficial de Python y realiza las siguientes configuraciones:
1. Instala dependencias desde `requirements.txt`.
2. Configura variables de entorno necesarias.
3. Define el comando de ejecución para iniciar la aplicación.

---

### **Configuración de pruebas**
Las pruebas se ejecutan automáticamente con cada `push` en el repositorio principal. Incluyen:
- Construcción del clúster completo.
- Validación de las peticiones API implementadas en la aplicación.
- Comprobación de la persistencia de datos en MongoDB.

## 🪵 Gestión de Logs
### **📂 Ubicación de los Logs**
- **Carpeta:** `logs/` (para entorno local).
- **Archivo:** `logs/watchit.log` (en entorno local) o temporal en `/tmp` (en entorno de testing).

### **📚 Ejemplo de Logs**
```plaintext
2025-01-03 08:10:12,345 - WatchIT - INFO - Fetching all movies
2025-01-03 08:11:45,678 - WatchIT - INFO - Attempting to add new movie: {'title': 'Matrix', 'genre': 'Sci-Fi', 'rating': 9.0}
2025-01-03 08:12:10,123 - WatchIT - INFO - Successfully added movie with ID: 5
2025-01-03 08:12:50,456 - WatchIT - ERROR - Error fetching movie with ID: 999 (Movie not found)
```
## 🌐 Enlaces importantes

### **Archivos relevantes del proyecto**
- [Dockerfile](../../Dockerfile): Configuración del contenedor de la aplicación WatchIT.
- [docker-compose.yaml](../../docker-compose.yaml): Configuración del clúster de contenedores.
- [requirements.txt](../../requirements.txt): Dependencias necesarias para ejecutar la aplicación.
- [app.py](../../src/app.py): Código principal de la aplicación.
- [movie_service.py](../../src/services/movie_service.py): Lógica de negocio para la gestión de películas.
- [test_app.py](../../tests/test_app.py): Pruebas automatizadas de la API.

### Configuración y publicación en GitHub Packages

Se ha configurado el repositorio para publicar automáticamente la imagen Docker de la aplicación en GitHub Packages. Para garantizar el correcto funcionamiento, se han tomado las siguientes medidas:

1. **Configuración del token de acceso:**
   - Se ha creado un Personal Access Token (PAT) con los permisos necesarios (`write:packages`, `delete:packages`) para permitir la publicación y administración de paquetes desde GitHub Actions.
   - Este token ha sido almacenado de manera segura.

2. **Publicación automática en GitHub Packages:**
   - La imagen Docker de la aplicación (`watchit`) se genera y publica automáticamente en GitHub Packages cada vez que se actualiza la rama principal (`main`) del repositorio.
   - Esto asegura que siempre se disponga de la última versión de la aplicación lista para su despliegue.

3. **Estado del paquete:**
   - La imagen `watchit` ha sido publicada correctamente en GitHub Packages como se muestra en las capturas adjuntas.


- **Listado de paquetes disponibles en el repositorio:**
  ![image](https://github.com/user-attachments/assets/1dabe23f-5de6-4f63-9103-cce1af8e7d08)

- **Detalles del paquete `watchit`:**
  ![image](https://github.com/user-attachments/assets/0ed15a82-2ad0-4715-9e41-a5fbd7cd5966)





