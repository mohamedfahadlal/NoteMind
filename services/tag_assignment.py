from services.tag_service import extract_tags

from models.note_model import (
    create_tag,
    get_tag_by_name,
    assign_tag
)


def auto_assign_tags(
    note_id,
    content
):

    tags = extract_tags(content)

    for tag in tags:

        create_tag(tag)

        db_tag = get_tag_by_name(tag)

        if db_tag:

            assign_tag(
                note_id,
                db_tag["id"]
            )


