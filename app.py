from flask import Flask,session,redirect

from routes.auth_routes import auth_bp

app = Flask(__name__)

app.secret_key = "notemind_secret_key"

app.register_blueprint(
    auth_bp
)


@app.route("/")
def home():
    return redirect("/login")

@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect("/login")

    return f"""
    Welcome {session['user_name']}
    <br><br>
    <a href='/logout'>Logout</a>
    """


if __name__ == "__main__":
    app.run(debug=True)
