# 🍿WatchIT📽️ - Hito 2

Este hito tiene como objetivo implementar las pruebas básicas de integración continua para WatchIT, una plataforma de gestión y recomendación de series y películas.

## Estructura del Proyecto

- `src/`: Contiene el backend de la aplicación en Flask.
- `tests/`: Contiene los tests.
- `.github/workflows/`: Configuración para integración continua con GitHub Actions.

## Dependencias

Las dependencias del proyecto están listadas en `requirements.txt` e incluyen:

- `flask`: Framework para el backend
- `pytest`: Biblioteca para ejecutar las pruebas

## Integración Continua

Se ha configurado GitHub Actions para ejecutar automáticamente los tests definidos en la carpeta `tests/` cada vez que se haga un push o pull request en la rama `main`.
