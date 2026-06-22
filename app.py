from flask import Flask,session,redirect,render_template

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

    return render_template(
        "dashboard.html",
        user_name=session["user_name"]
    )

@app.route("/upload")
def upload():

    if "user_id" not in session:
        return redirect("/login")

    return "Upload Page Coming Soon"


@app.route("/my-notes")
def my_notes():

    if "user_id" not in session:
        return redirect("/login")

    return "My Notes Page Coming Soon"
if __name__ == "__main__":
    app.run(debug=True)
