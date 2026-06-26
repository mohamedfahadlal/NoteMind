from services.category_service import categorize_note

from models.note_model import (
    assign_category,
    get_category_id_by_name
)


def auto_assign_category(
    note_id,
    content
):

    category_name = categorize_note(
        content
    )

    if not category_name:
        return

    category = get_category_id_by_name(
        category_name
    )

    if not category:
        return

    assign_category(
        note_id,
        category["id"]
    )
