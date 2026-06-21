from flask import (
    Blueprint,
    render_template,
    request
)

from services.auth_service import register_user

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
