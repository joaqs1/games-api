import sqlite3
from flask import Flask, jsonify, request, g

app = Flask(__name__)
DATABASE = "games.db"
REQUIRED_FIELDS = ["title", "genre", "platform", "release_year"]

SEED_GAMES = [
    ("Hollow Knight", "Metroidvania", "PC", 2017, 9.4),
    ("Stardew Valley", "Simulation", "PC", 2016, 9.1),
    ("Celeste", "Platformer", "Switch", 2018, 9.0),
    ("The Legend of Zelda: Breath of the Wild", "Action-Adventure", "Switch", 2017, 9.7),
    ("Minecraft", "Sandbox", "PC", 2011, 9.3),
    ("Portal 2", "Puzzle", "PC", 2011, 9.5),
    ("Elden Ring", "Action RPG", "PlayStation 5", 2022, 9.6),
    ("Undertale", "RPG", "PC", 2015, 9.2),
    ("Mario Kart 8 Deluxe", "Racing", "Switch", 2017, 9.0),
    ("Hades", "Roguelike", "PC", 2020, 9.3),
    ("God of War", "Action-Adventure", "PlayStation 4", 2018, 9.4),
    ("Among Us", "Party", "Mobile", 2018, 8.2),
]


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(exc):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    db = sqlite3.connect(DATABASE)
    db.execute(
        """CREATE TABLE IF NOT EXISTS games (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            genre TEXT NOT NULL,
            platform TEXT NOT NULL,
            release_year INTEGER NOT NULL,
            rating REAL
        )"""
    )
    if db.execute("SELECT COUNT(*) FROM games").fetchone()[0] == 0:
        db.executemany(
            "INSERT INTO games (title, genre, platform, release_year, rating) VALUES (?,?,?,?,?)",
            SEED_GAMES,
        )
    db.commit()
    db.close()


def validate(data):
    """Return an error message string, or None if the data is valid."""
    if not isinstance(data, dict):
        return "Request body must be a JSON object"
    missing = [f for f in REQUIRED_FIELDS if data.get(f) in (None, "")]
    if missing:
        return f"Missing required field(s): {', '.join(missing)}"
    if not isinstance(data["release_year"], int):
        return "release_year must be an integer"
    if data.get("rating") is not None and not isinstance(data["rating"], (int, float)):
        return "rating must be a number"
    return None


def find_game(game_id):
    row = get_db().execute("SELECT * FROM games WHERE id = ?", (game_id,)).fetchone()
    return dict(row) if row else None


@app.get("/games")
def list_games():
    rows = get_db().execute("SELECT * FROM games").fetchall()
    return jsonify([dict(r) for r in rows]), 200


@app.get("/games/<int:game_id>")
def get_game(game_id):
    game = find_game(game_id)
    if not game:
        return jsonify({"error": f"Game with id {game_id} not found"}), 404
    return jsonify(game), 200


@app.post("/games")
def create_game():
    data = request.get_json(silent=True)
    error = validate(data)
    if error:
        return jsonify({"error": error}), 400
    db = get_db()
    cur = db.execute(
        "INSERT INTO games (title, genre, platform, release_year, rating) VALUES (?,?,?,?,?)",
        (data["title"], data["genre"], data["platform"], data["release_year"], data.get("rating")),
    )
    db.commit()
    return jsonify(find_game(cur.lastrowid)), 201


@app.put("/games/<int:game_id>")
def update_game(game_id):
    if not find_game(game_id):
        return jsonify({"error": f"Game with id {game_id} not found"}), 404
    data = request.get_json(silent=True)
    error = validate(data)
    if error:
        return jsonify({"error": error}), 400
    db = get_db()
    db.execute(
        "UPDATE games SET title=?, genre=?, platform=?, release_year=?, rating=? WHERE id=?",
        (data["title"], data["genre"], data["platform"], data["release_year"], data.get("rating"), game_id),
    )
    db.commit()
    return jsonify(find_game(game_id)), 200


@app.delete("/games/<int:game_id>")
def delete_game(game_id):
    if not find_game(game_id):
        return jsonify({"error": f"Game with id {game_id} not found"}), 404
    db = get_db()
    db.execute("DELETE FROM games WHERE id = ?", (game_id,))
    db.commit()
    return jsonify({"message": f"Game {game_id} deleted"}), 200


if __name__ == "__main__":
    init_db()
    app.run(debug=True)