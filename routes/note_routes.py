from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    session,
    current_app
)

from services.note_service import save_note

note_bp = Blueprint(
    "notes",
    __name__
)


@note_bp.route(
    "/upload",
    methods=["GET", "POST"]
)
def upload():

    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":

        title = request.form["title"]

        uploaded_file = request.files["file"]

        success = save_note(
            uploaded_file,
            title,
            session["user_id"],
            current_app.config["UPLOAD_FOLDER"]
        )

        if success:
            return redirect("/my-notes")

        return "Invalid File Type"

    return render_template(
        "upload.html"
    )