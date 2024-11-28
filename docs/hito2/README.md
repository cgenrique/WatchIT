# 🍿WatchIT📽️ - Hito 2

Este hito tiene como objetivo implementar las pruebas básicas de integración continua para WatchIT, una plataforma de gestión y recomendación de series y películas.

## Objetivos

1. Configurar un entorno básico de pruebas usando `pytest`.
2. Crear una estructura de datos inicial usando archivos JSON en lugar de una base de datos.
3. Implementar integración continua usando **GitHub Actions**.

## 📂Estructura del Proyecto

- `src/`: Contiene el backend de la aplicación en Flask.
- `tests/`: Contiene los tests con Pytest.
- `.github/workflows/`: Configuración para integración continua con GitHub Actions.

## ⚙️Dependencias

Las dependencias del proyecto están listadas en `requirements.txt` e incluyen entre otras:

- `flask`: Framework para el backend
- `pytest`: Biblioteca para ejecutar las pruebas

Instala las dependencias ejecutando:

```bash
pip install -r requirements.txt
```

## 🤖Integración Continua

Se ha configurado GitHub Actions para ejecutar automáticamente los tests definidos en la carpeta `tests/` cada vez que se haga un push o pull request en la rama `main`.

## ¿Por qué GitHub Actions?

- **Integración nativa:** Está directamente integrado en GitHub, lo que simplifica la configuración.
- **Gratuito para repositorios públicos:** Ideal para proyectos de código abierto.
- **Escalabilidad:** Soporta múltiples lenguajes y configuraciones.
