from flask import Flask, session, redirect, render_template
from routes.auth_routes import auth_bp
from routes.note_routes import note_bp
import os

app = Flask(__name__)

app.secret_key = os.environ.get("FLASK_SECRET_KEY", "notemind_secret_key")

app.register_blueprint(auth_bp)
app.register_blueprint(note_bp)

BASE_DIR = os.path.abspath(
    os.path.dirname(__file__)
)

UPLOAD_FOLDER = os.path.join(
    BASE_DIR,
    "uploads"
)

os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/")
def home():
    return redirect("/login")

@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect("/login")

    return render_template(
        "dashboard.html",
        user_name=session["user_name"]
    )


@app.cli.command("init-db")
def init_db_command():
    """Initialize database schema, tables, and default seed data."""
    from database.init_db import init_db
    success = init_db()
    if not success:
        raise SystemExit(1)


@app.cli.command("migrate-db")
def migrate_db_command():
    """Apply any pending database migrations."""
    from database.migrations import run_migrations
    _, success = run_migrations()
    if not success:
        raise SystemExit(1)


if __name__ == "__main__":
    app.run(debug=True)
