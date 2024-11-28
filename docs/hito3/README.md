# 🍿WatchIT📽️ - Hito 3

Este hito tiene como objetivo principal diseñar y estructurar un microservicio basado en la funcionalidad del Hito 2. Incluye la separación de la lógica de negocio, validaciones exhaustivas y pruebas, mejorando la calidad del backend de la plataforma WatchIT.

## 🚀 Objetivos
- Separar la lógica de negocio de la API para lograr un diseño modular y profesional.
- Implementar validaciones estrictas.
- Añadir nuevos tests que aseguren el correcto funcionamiento de las rutas y validaciones.
- Facilitar la depuración y el monitoreo mediante logs.

## 🔨 Cambios realizados
1. **Refactorización**:
   - He separado la lógica de negocio en una clase independiente (`MovieService`).
   - Además he añadido el manejo de errores para datos incompletos o inválidos.

**Ejemplo: Antes (lógica y API mezcladas):**
```python
@app.route('/movies', methods=['POST'])
def add_movie():
    new_movie = request.get_json()
    movies = load_data()
    new_movie['id'] = len(movies) + 1
    movies.append(new_movie)
    save_data(movies)
    return jsonify(new_movie), 201
```

**Ejemplo: Después (lógica separada)**
```python
# app.py
@app.route('/movies', methods=['POST'])
def add_movie():
    """
    Endpoint to add a new movie to the list.

    Returns:
        JSON: The newly added movie data.
    """
    
    try:
        new_movie = request.get_json()
        added_movie = movie_service.add_movie(new_movie)
        return jsonify(added_movie), 201
    
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
```

```python
# movie_service.py
def add_movie(self, new_movie):
        """
        Add a new movie.

        Args:
            new_movie (dict): Movie data to add.

        Returns:
            dict: The newly added movie data.
        
        Raises:
            ValueError: If the movie data is invalid.
        """
        # Check if the movie data is valid
        required_fields = ["title", "genre", "rating"]
        for field in required_fields:
            if field not in new_movie:
                raise ValueError(f"Missing required field: {field}")
        
        # Check if the rating is between 0 and 10
        rating = new_movie["rating"]
        if not (0 <= rating <= 10):
            raise ValueError("Rating must be between 0 and 10")
        
        # If the data is valid, add the movie
        movies = self.load_data()
        new_movie['id'] = len(movies) + 1
        movies.append(new_movie)
        self.save_data(movies)
        return new_movie
```


