from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    session,
    current_app,
    send_file
)

from services.note_service import save_note,fetch_user_notes,fetch_note,fetch_note_category,fetch_note_tags,search_user_notes

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

@note_bp.route("/my-notes")
def my_notes():

    if "user_id" not in session:
        return redirect("/login")

    notes = fetch_user_notes(session["user_id"])

    for note in notes:

        category = fetch_note_category(note["id"])

        note["category"] = (category["name"] if category else "Uncategorized")

        tags = fetch_note_tags(note["id"])

        note["tags"] = ", ".join(tag["tag_name"]for tag in tags)

        return render_template("my_notes.html",notes=notes)

@note_bp.route("/note/<int:note_id>")
def open_note(note_id):

    if "user_id" not in session:
        return redirect("/login")

    note = fetch_note(note_id)

    if not note:
        return "Note not found"

    if note["user_id"] != session["user_id"]:
        return "Access Denied"

    return send_file(
        note["file_path"]
    )
@note_bp.route("/search")
def search():

    if "user_id" not in session:
        return redirect("/login")

    query = request.args.get(
        "q",
        ""
    )

    notes = []

    if query:

        notes = search_user_notes(
            session["user_id"],
            query
        )

    return render_template(
        "search.html",
        notes=notes,
        query=query
    )

