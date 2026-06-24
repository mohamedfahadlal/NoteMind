import os

from werkzeug.utils import secure_filename

from models.note_model import create_note,get_notes_by_user,get_note_by_id



ALLOWED_EXTENSIONS = {
    "pdf",
    "docx",
    "txt"
}


def allowed_file(filename):

    return (
        "." in filename
        and
        filename.rsplit(".", 1)[1].lower()
        in ALLOWED_EXTENSIONS
    )


def save_note(
    uploaded_file,
    title,
    user_id,
    upload_folder
):

    if not allowed_file(
        uploaded_file.filename
    ):
        return False

    filename = secure_filename(
        uploaded_file.filename
    )

    filepath = os.path.join(
        upload_folder,
        filename
    )

    uploaded_file.save(filepath)

    file_type = filename.split(".")[-1]

    create_note(
        user_id,
        title,
        filename,
        filepath,
        file_type
    )

    return True

def fetch_user_notes(user_id):

    return get_notes_by_user(user_id)

def fetch_note(note_id):

    return get_note_by_id(note_id)
