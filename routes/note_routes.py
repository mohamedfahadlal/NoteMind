from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    session,
    current_app,
    send_file
)

from services.note_service import save_note,fetch_user_notes,fetch_note,fetch_note_category,fetch_note_tags,search_user_notes,search_by_category,fetch_categories,fetch_tags,search_by_tag,fetch_summary,answer_question,fetch_similar_notes

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

    query = request.args.get("q", "").strip()
    category = request.args.get("category", "")

    tag = request.args.get("tag","")

    categories = fetch_categories()

    tags = fetch_tags()

    notes = []

    if tag:

        notes = search_by_tag(
            session["user_id"],
            int(tag)
        )

    elif category:

        notes = search_by_category(
            session["user_id"],
            int(category)
        )

    elif query:

        notes = search_user_notes(
            session["user_id"],
            query
        )

    for note in notes:

        category = fetch_note_category(
            note["id"]
        )

        note["category"] = (
            category["name"]
            if category
            else "Uncategorized"
        )

        tags = fetch_note_tags(
            note["id"]
        )

        note["tags"] = ", ".join(
            tag["tag_name"]
            for tag in tags
        )

    return render_template(
    "search.html",
    notes=notes,
    query=query,
    categories=categories,
    tags=tags,
    selected_category=category,
    selected_tag=tag
)

@note_bp.route("/summary/<int:note_id>")
def view_summary(note_id):

    if "user_id" not in session:
        return redirect("/login")


    note = fetch_note(note_id)


    if not note:
        return "Note not found"


    if note["user_id"] != session["user_id"]:
        return "Access Denied"


    summary = fetch_summary(
        note_id
    )


    return render_template(
        "summary.html",
        note=note,
        summary=summary
    )


@note_bp.route(
    "/question/<int:note_id>",
    methods=["GET", "POST"]
)
def ask_question(note_id):

    if "user_id" not in session:
        return redirect("/login")

    note = fetch_note(note_id)

    if not note:
        return "Note not found"

    if note["user_id"] != session["user_id"]:
        return "Access Denied"

    answer = None
    question = ""

    if request.method == "POST":

        question = request.form["question"].strip()

        answer = answer_question(
            note_id,
            question
        )

    return render_template(
    "question.html",
    note=note,
    question=question,
    answer=answer
)


@note_bp.route("/note-info/<int:note_id>")
def note_info(note_id):

    if "user_id" not in session:
        return redirect("/login")

    note = fetch_note(note_id)

    if not note:
        return "Note not found"

    if note["user_id"] != session["user_id"]:
        return "Access Denied"

    similar_notes = fetch_similar_notes(
        note_id,
        session["user_id"]
    )

    return render_template(
        "note_info.html",
        note=note,
        similar_notes=similar_notes
    )