from flask import Flask

from routes.auth_routes import auth_bp

app = Flask(__name__)

app.secret_key = "notemind_secret_key"

app.register_blueprint(
    auth_bp
)


@app.route("/")
def home():
    return "Welcome to NoteMind"


if __name__ == "__main__":
    app.run(debug=True)
