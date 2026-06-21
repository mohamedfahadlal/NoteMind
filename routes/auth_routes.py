from flask import (
    Blueprint,
    render_template,
    request,
    session,
    redirect,
    url_for
)
from services.auth_service import register_user,login_user

auth_bp = Blueprint(
    "auth",
    __name__
)


@auth_bp.route(
    "/register",
    methods=["GET", "POST"]
)
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        register_user(
            name,
            email,
            password
        )

        return "Registration Successful"

    return render_template(
        "register.html"
    )

@auth_bp.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        user = login_user(
            email,
            password
        )

        if user:

            session["user_id"] = user["id"]
            session["user_name"] = user["name"]

            return redirect("/dashboard")

        return "Invalid Credentials"

    return render_template("login.html")

@auth_bp.route("/logout")
def logout():

    session.clear()

    return redirect("/login")
