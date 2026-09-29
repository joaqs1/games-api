# Video Games REST API

A simple CRUD API built with Flask and SQLite.

## Setup

```bash
pip install flask
python app.py
```

Server runs at `http://127.0.0.1:5000`. The database (`games.db`) is created and seeded with 12 games on first run.

## Data model

| Field | Type | Required |
|---|---|---|
| id | integer (auto) | - |
| title | string | yes |
| genre | string | yes |
| platform | string | yes |
| release_year | integer | yes |
| rating | number | no |

## Endpoints

### GET /games
Returns all games. **200**

```bash
curl http://127.0.0.1:5000/games
```
```json
[{"id": 1, "title": "Hollow Knight", "genre": "Metroidvania", "platform": "PC", "release_year": 2017, "rating": 9.4}]
```

### GET /games/:id
Returns one game. **200**, or **404** if not found.

```bash
curl http://127.0.0.1:5000/games/1
```
```json
{"id": 1, "title": "Hollow Knight", "genre": "Metroidvania", "platform": "PC", "release_year": 2017, "rating": 9.4}
```

### POST /games
Creates a game. **201**, or **400** if a required field is missing or invalid.

```bash
curl -X POST http://127.0.0.1:5000/games -H "Content-Type: application/json" -d '{"title":"Portal","genre":"Puzzle","platform":"PC","release_year":2007,"rating":9.0}'
```
```json
{"id": 13, "title": "Portal", "genre": "Puzzle", "platform": "PC", "release_year": 2007, "rating": 9.0}
```

Error example (400):
```json
{"error": "Missing required field(s): genre, platform, release_year"}
```

### PUT /games/:id
Updates a game. All required fields must be sent. **200**, **400**, or **404**.

```bash
curl -X PUT http://127.0.0.1:5000/games/13 -H "Content-Type: application/json" -d '{"title":"Portal","genre":"Puzzle","platform":"PC","release_year":2007,"rating":9.5}'
```
```json
{"id": 13, "title": "Portal", "genre": "Puzzle", "platform": "PC", "release_year": 2007, "rating": 9.5}
```

### DELETE /games/:id
Deletes a game. **200**, or **404** if not found.

```bash
curl -X DELETE http://127.0.0.1:5000/games/13
```
```json
{"message": "Game 13 deleted"}
```

## Status codes

| Code | Meaning |
|---|---|
| 200 | Successful read, update, or delete |
| 201 | Successful create |
| 400 | Bad request (missing or invalid field) |
| 404 | Game not found |