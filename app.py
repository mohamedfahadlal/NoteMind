from flask import Flask

app = Flask(__name__)

app.secret_key = "notemind_secret_key"


@app.route("/")
def home():
    return "Welcome to NoteMind"


if __name__ == "__main__":
    app.run(debug=True)