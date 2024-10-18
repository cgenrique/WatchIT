# 🍿WatchIT📽️ - Hito 1

Como ya se describe en el [README](../README.md) del repositorio. Se realizará el desarrollo de una plataforma que permita a cinéfilos y seriéfilos la organización de sus títulos favoritos. Además de recomendarles contenido en función de sus preferencias.

El Hito 1 del proyecto **WatchIT** consiste en la creación del repositorio de prácticas, la configuración del entorno de desarrollo, y la definición del problema que se va a resolver. Aquí se establecerá la estructura inicial del repositorio.


## Descripción del Problema😵‍💫
**WatchIT** busca solucionar el excesivo tiempo que pasan los usuarios eligiendo un contenido audiovisual que ver en su tiempo libre. Debido a la gran cantidad de películas y series disponibles actualmente, la elección de una opción puede resultar abrudamora. 

Además, poder clasificar el contenido que se quiere ver, se ha visto o que nos gusta especialmente puede facilitar el proceso de seleccion de contenido.

## Funcionalidades principales
Las funcionalidades principales de la plataforma son:
 - **Gestión de listas**: Permitir a los usuarios crear listas de películas y series para organizar el contenido que quieren ver o que ya han visto
 - **Búsqueda y filtrado de títulos**: Permitir la búsqueda y filtrado de títulos por parte del usuario
 - **Información de títulos**: Proporcionar una vista de la información más relevante de una serie o película (sinopsis, reparto, calificación...)

## Tipos de usuarios👥
 Existen dos tipos principales de usuarios en la plataforma:
  - **Usuario espectador (estándar)**: Que además de registrarse e iniciar sesión. Puede gestionar sus listas de series y películas.
  - **Usuario administrador**: Puede añadir, eliminar o modificar títulos dentro de la plataforma. Gestionar las categorías.

De esta manera, algunas de las funcionalidades que ofrece WatchIT son:
- Organizar y gestionar las series y películas en listas personalizadas
- Acceder a recomendaciones de series y películas en base a nuestras preferencias
- Acceder a información detallada sobre series y películas


## Tecnologías a utilizar🖥️

Se ha optado para el desarrollo de la aplicación por una aquitectura de tipo cliente-servidor con servicios. Para la implementación de la API se optará por **Python** y **Flask**

En cuanto a la base de datos, se opta por una BD de tipo NoSQL como es el caso de **MongoDB**. Siendo flexible para los diferentes tipos de esquemas de datos (ya que algunos títulos pueden contener más información que otros).

Se hará uso de la API de [TMDb (The Movie Database)](https://www.themoviedb.org/documentation/api). Esta API gratuita nos proporciona datos sobre gran variedad de series y películas.

En lo relativo al frontend, se intentará realizarlo haciendo uso de React.

## Configuración del entorno⚙️

En cuanto a la configuración del entorno de trabajo. Se ha configurado tanto el nombre como el email que se va a usar en git.

![image](https://github.com/user-attachments/assets/2952f685-6c6f-4788-90e9-601f603b3294)

Se han implementado las claves de acceso remoto (SSH) para poder subir los cambios al repositorio con facilidad.

![image](https://github.com/user-attachments/assets/05c27701-11b5-4e7c-a77a-9143bb90f508)

También está completa la información del perfil de github, con foto y nombre completo.

![image](https://github.com/user-attachments/assets/75445d11-1772-4965-b5ef-4c6764d04406)

También está configurado el doble factor de autentificación cuando se inicia sesión. Haciendo uso de una aplicación móvil de generación de códigos para autenficicación (Google Authenticator)

![image](https://github.com/user-attachments/assets/1f16cb0f-fedf-4f92-ba91-cd5fec6dbe43)

