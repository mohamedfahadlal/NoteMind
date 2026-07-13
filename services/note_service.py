import os

from werkzeug.utils import secure_filename

from models.note_model import create_note,get_notes_by_user,get_note_by_id,update_note_content,get_note_category,get_note_tags,search_notes,save_search_history,get_all_categories,search_notes_by_category,get_all_tags,search_notes_by_tag,save_summary,get_summary
from services.text_extractor import extract_txt,extract_docx,extract_pdf
from services.category_assignment import auto_assign_category
from services.tag_assignment import auto_assign_tags
from services.summary_service import generate_summary

from services.question_service import find_best_paragraph


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


def save_note(uploaded_file,title,user_id,upload_folder):

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

    note_id = create_note(user_id,title,filename,filepath,file_type)

    content = None

    if file_type == "txt":

        content = extract_txt(filepath)

    elif file_type == "docx":

        content = extract_docx(filepath)

    elif file_type == "pdf":

        content = extract_pdf(filepath)

    if content:

        update_note_content(note_id,content)

        auto_assign_category(note_id,content)

        auto_assign_tags(note_id,content)

        summary = generate_summary(content)
        save_summary(note_id,summary)
    return True

def fetch_user_notes(user_id):

    return get_notes_by_user(user_id)

def fetch_note(note_id):

    return get_note_by_id(note_id)



def fetch_note_category(note_id):

    return get_note_category(note_id)

def fetch_note_tags(note_id):

    return get_note_tags(note_id)


def search_user_notes(
    user_id,
    query
):

    save_search_history(
        user_id,
        query
    )

    return search_notes(
        user_id,
        query
    )

def fetch_categories():

    return get_all_categories()

def search_by_category(
    user_id,
    category_id
):

    return search_notes_by_category(
        user_id,
        category_id
    )


def fetch_tags():

    return get_all_tags()


def search_by_tag(
    user_id,
    tag_id
):

    return search_notes_by_tag(
        user_id,
        tag_id
    )


def fetch_summary(note_id):

    return get_summary(note_id)


def answer_question(
    note_id,
    question
):

    note = get_note_by_id(
        note_id
    )

    if not note:
        return "Note not found."

    if not note["content"]:
        return "This note does not contain extracted text."

    answer = find_best_paragraph(
        note["content"],
        question
    )

    if not answer:
        return "Sorry, I couldn't find an answer to that question in this note."

    return answer