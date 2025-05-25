from flask import Flask, request, jsonify
import os
import sqlite3
from datetime import datetime

app = Flask(__name__)
DB_PATH = 'models.db'
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS models (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            version TEXT NOT NULL,
            accuracy REAL NOT NULL,
            timestamp TEXT NOT NULL
        )
        """)
init_db()

@app.route("/models", methods=["POST"])
def upload_model():
    model_file = request.files.get("file")
    name = request.form.get("name")
    version = request.form.get("version")
    accuracy = request.form.get("accuracy")

    if not model_file or not name or not version or not accuracy:
        return jsonify({"error": "Missing required fields"}), 400

    filepath = os.path.join(UPLOAD_FOLDER, model_file.filename)
    model_file.save(filepath)

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "INSERT INTO models (name, version, accuracy, timestamp) VALUES (?, ?, ?, ?)",
            (name, version, float(accuracy), datetime.utcnow().isoformat())
        )

    return jsonify({"message": "Model registered successfully"}), 201

@app.route("/models", methods=["GET"])
def list_models():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute("SELECT name, version, accuracy, timestamp FROM models")
        models = [dict(zip(["name", "version", "accuracy", "timestamp"], row)) for row in cursor.fetchall()]
    return jsonify(models)

@app.route("/models/<string:name>", methods=["GET"])
def get_model(name):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute("SELECT name, version, accuracy, timestamp FROM models WHERE name = ?", (name,))
        row = cursor.fetchone()
        if not row:
            return jsonify({"error": "Model not found"}), 404
        return jsonify(dict(zip(["name", "version", "accuracy", "timestamp"], row)))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
