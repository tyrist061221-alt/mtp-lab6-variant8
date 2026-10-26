"""Повыш.1 — Flask-приложение с базой SQLite (CRUD «Заметки»).

Create  — POST /add
Read    — GET  /
Update  — GET/POST /edit/<id>
Delete  — POST /delete/<id>

Запуск:  python -m tasks.povysh_1_flask_sqlite   ->  http://127.0.0.1:5000/
"""
import sqlite3
from datetime import datetime
from pathlib import Path

from flask import Flask, abort, g, redirect, render_template, request, url_for
from pydantic import ValidationError

from tasks.schemas import NoteIn

BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_DB = BASE_DIR / "notes.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    text TEXT NOT NULL DEFAULT '',
    created_at TEXT NOT NULL
)
"""


def create_app(db_path=DEFAULT_DB) -> Flask:
    app = Flask(
        __name__,
        template_folder=str(BASE_DIR / "templates"),
        static_folder=str(BASE_DIR / "static"),
    )
    app.config["DATABASE"] = str(db_path)

    def get_db() -> sqlite3.Connection:
        if "db" not in g:
            g.db = sqlite3.connect(app.config["DATABASE"])
            g.db.row_factory = sqlite3.Row
        return g.db

    @app.teardown_appcontext
    def close_db(_exc):
        db = g.pop("db", None)
        if db is not None:
            db.close()

    conn = sqlite3.connect(app.config["DATABASE"])
    conn.execute(SCHEMA)
    conn.commit()
    conn.close()

    def validation_errors(exc: ValidationError) -> list:
        return [f"{'.'.join(map(str, e['loc']))}: {e['msg']}" for e in exc.errors()]

    def all_notes():
        return get_db().execute("SELECT * FROM notes ORDER BY id DESC").fetchall()

    # ----- READ -----
    @app.route("/")
    def index():
        return render_template("notes.html", notes=all_notes(), errors=[])

    # ----- CREATE -----
    @app.route("/add", methods=["POST"])
    def add():
        try:
            data = NoteIn(
                title=request.form.get("title", ""), text=request.form.get("text", "")
            )
        except ValidationError as exc:
            return render_template(
                "notes.html", notes=all_notes(), errors=validation_errors(exc)
            ), 400
        db = get_db()
        db.execute(
            "INSERT INTO notes (title, text, created_at) VALUES (?, ?, ?)",
            (data.title, data.text, datetime.now().isoformat(timespec="seconds")),
        )
        db.commit()
        return redirect(url_for("index"))

    # ----- UPDATE -----
    @app.route("/edit/<int:note_id>", methods=["GET", "POST"])
    def edit(note_id: int):
        db = get_db()
        note = db.execute("SELECT * FROM notes WHERE id = ?", (note_id,)).fetchone()
        if note is None:
            abort(404)
        if request.method == "POST":
            try:
                data = NoteIn(
                    title=request.form.get("title", ""), text=request.form.get("text", "")
                )
            except ValidationError as exc:
                return render_template(
                    "edit.html", note=note, errors=validation_errors(exc)
                ), 400
            db.execute(
                "UPDATE notes SET title = ?, text = ? WHERE id = ?",
                (data.title, data.text, note_id),
            )
            db.commit()
            return redirect(url_for("index"))
        return render_template("edit.html", note=note, errors=[])

    # ----- DELETE -----
    @app.route("/delete/<int:note_id>", methods=["POST"])
    def delete(note_id: int):
        db = get_db()
        cur = db.execute("DELETE FROM notes WHERE id = ?", (note_id,))
        db.commit()
        if cur.rowcount == 0:
            abort(404)
        return redirect(url_for("index"))

    return app


if __name__ == "__main__":
    create_app().run(debug=True)
