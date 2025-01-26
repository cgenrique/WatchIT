# 🍿 WatchIT 📽️ - Hito 5

En este hito, se ha desplegado la aplicación en la nube (en un PaaS), haciéndola accesible desde cualquier dispositivo.

## 🚀 Objetivos
- Desplegar la aplicación en la nube usando un PaaS (Plataforma como Servicio).
- Configurar un flujo automatizado que permita desplegar la aplicación directamente desde un push al repositorio.


## 🔨 Cambios realizados

### **1. Funcionalidades básicas iniciales**
Hasta este momento, las funcionalidades de la aplicación eran muy limitadas, restringiéndose a varios endpoints que permitían:
- ➕A ñadir películas a la base de datos.
- ✏️ Editar películas en la base de datos.
- ❌ Eliminar películas de la base de datos.

### **2. Integración con la API de TMDb**
Se ha integrado la aplicación con la [🌐 API de TMDb](https://www.themoviedb.org/) para obtener información detallada de las películas. Esto ha permitido que:
- 🔎 Los usuarios puedan buscar películas directamente desde TMDb.
- 📋 Se muestren detalles como el título, descripción, fecha de lanzamiento y póster de las películas obtenidos de la API.
- 📦 Simplifique la gestión de las películas al no depender de datos manuales almacenados en la base de datos.

### **3. Sistema de usuarios**
Se ha implementado un sistema básico de usuarios con las siguientes características:
- 📝 Registro de nuevos usuarios.
- 🔐 Inicio de sesión con autenticación basada en tokens JWT.
- 🎞️ Gestión de listas personales de películas (favoritas, vistas, pendientes).
- Actualmente, todos los usuarios tienen el rol de `user`. En el futuro, se planea añadir roles como `admin` y las funcionalidades específicas para estos.

### **4. Frontend básico**
- 🌟 Se ha desarrollado un frontend funcional usando templates HTML con estilos básicos en CSS.
- Aunque es una interfaz simple, permite a los usuarios realizar las acciones principales como buscar películas y gestionar sus listas.
- 💻 En un futuro, se considera rediseñar el frontend utilizando **React** para una experiencia más dinámica y moderna.


### **5. Despliegue en la nube**
Tras implementar las funcionalidades básicas mencionadas, se procedió a desplegar la aplicación en la nube utilizando **Render** como plataforma PaaS. Este despliegue incluye:
- ☁️ La conexión a la base de datos **MongoDB Atlas** para el almacenamiento de datos.
- ⚙️ Configuración de las variables de entorno necesarias para el funcionamiento de la aplicación en un entorno en la nube.
- ✅ Pruebas básicas para garantizar que las funcionalidades implementadas funcionan correctamente en el entorno de producción.

---

## 🌐 Despliegue de la aplicación

### **1. Elección de Render como PaaS**
Para el despliegue de la aplicación, se seleccionó **Render** como plataforma PaaS debido a las siguientes ventajas:
- 🛠️ **Simplicidad**: Render ofrece una interfaz intuitiva y una configuración rápida para desplegar aplicaciones directamente desde un repositorio de GitHub.
- 💸 **Gratuito**: Permite el despliegue gratuito de servicios web, ideal para el propósito académico y el desarrollo inicial de aplicaciones.
- 📈 **Escalabilidad**: Render permite escalar la aplicación fácilmente si en el futuro se requiere un entorno de producción más robusto.

### **2. Configuración en Render**
El proceso de despliegue en Render consistió en los siguientes pasos:
1. **Conexión del repositorio de GitHub**:
   - 🔗 Se vinculó el repositorio del proyecto a Render para permitir un despliegue automático con cada push a la rama principal.
2. **Configuración del servicio web**:
   - 🛠️ Se añadieron las variables de entorno necesarias para el correcto funcionamiento de la aplicación, como `DATABASE_URL` para conectar con MongoDB Atlas y el token de la API de TMDb.
3. **Despliegue automático**:
   - 🚀 Render se configuró para que, al detectar cambios en la rama principal del repositorio, se reconstruya y despliegue automáticamente la última versión de la aplicación.

![image](https://github.com/user-attachments/assets/2ccd1b88-88a9-41ad-896b-fae2305f7481)


### **3. Base de datos con MongoDB Atlas**
Para la base de datos, se optó por **MongoDB Atlas**, una solución en la nube que ofrece una configuración sencilla y compatibilidad total con nuestra aplicación. El proceso fue el siguiente:
1. **Creación del clúster**:
   - 🌍 Se creó un clúster gratuito en MongoDB Atlas con un tamaño adecuado para el proyecto y un rendimiento óptimo.
   - 🌐 Se configuró en la región europea correspondiente al despliegue en Render (Frankfurt). El cluster está en París.
2. **Gestión de usuarios y acceso**:
   - 👤 Se creó un usuario específico para la aplicación con los permisos necesarios para acceder al clúster.
   - 🔓 Se permitió el acceso desde cualquier IP para garantizar la conexión entre Render y MongoDB Atlas.
3. **Conexión con la aplicación**:
   - 🔗 Se obtuvo la URI de conexión de MongoDB Atlas.
   - ⚙️ Se añadió esta URI como la variable de entorno `DATABASE_URL` tanto en el entorno local como en Render.
   - 🖧 Se modificó la aplicación para que utilice esta URI para conectarse a la base de datos.

![image](https://github.com/user-attachments/assets/0a7a3831-b3a8-49d0-9cd8-663ded0ce4ab)


### **4. Integración y pruebas**
- 🧪 Una vez configurados Render y MongoDB Atlas, se realizaron pruebas para garantizar que la aplicación se conecta correctamente a la base de datos y que las funcionalidades principales (registro, login y gestión de listas) funcionan sin problemas en el entorno de producción.
- 🛠️ Además, se probó el despliegue automático desde GitHub para verificar que los cambios realizados en el código se reflejan correctamente en la aplicación desplegada.

### **5. Resultados del despliegue**
- 🌍 La aplicación está disponible públicamente a través de la URL proporcionada por Render: https://watchit-kzwe.onrender.com/
- ✅ Todas las funcionalidades básicas (registro, inicio de sesión, búsqueda de películas y gestión de listas) funcionan correctamente en el entorno de producción.
- 💾 MongoDB Atlas muestra los datos generados por la aplicación, lo que confirma la conexión y el almacenamiento exitoso.

### **6. Capturas de funcionalidades básicas**
A continuación, se presentan capturas del servicio desplegado en **Render**, mostrando las funcionalidades principales en funcionamiento:

#### **🔎 Búsqueda de películas**
- Pantalla de inicio con el búscador de películas.
![image](https://github.com/user-attachments/assets/a070427a-b2b0-4e3a-9450-56b62fa78732)

- Resultados de una búsqueda de películas
![image](https://github.com/user-attachments/assets/9485b344-c468-485f-958a-96322a816069)

#### **🎞️ Gestión de listas personales**
- Funcionalidad para añadir películas a listas personales como "Favoritos" o "Por ver".
![image](https://github.com/user-attachments/assets/5ba06a55-72cf-4a1c-b82b-a4a1147b39ea)

#### **🎞️ Detalles de una película**
- Detalles de una película (mediante la api de TMDb)
![image](https://github.com/user-attachments/assets/dc855522-4d68-41b8-b862-f43aa061e0bf)



