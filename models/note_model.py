from database.connection import get_db_connection


def create_note(
    user_id,
    title,
    file_name,
    file_path,
    file_type
):

    conn = get_db_connection()

    cursor = conn.cursor()

    query = """
    INSERT INTO notes
    (
        user_id,
        title,
        file_name,
        file_path,
        file_type
    )
    VALUES
    (
        %s,
        %s,
        %s,
        %s,
        %s
    )
    RETURNING id
    """

    cursor.execute(
        query,
        (
            user_id,
            title,
            file_name,
            file_path,
            file_type
        )
    )

    note_id = cursor.fetchone()["id"]

    conn.commit()

    cursor.close()
    conn.close()

    return note_id

def get_notes_by_user(user_id):

    conn = get_db_connection()

    cursor = conn.cursor()

    query = """
    SELECT *
    FROM notes
    WHERE user_id = %s
    ORDER BY uploaded_at DESC
    """

    cursor.execute(query, (user_id,))

    notes = cursor.fetchall()

    cursor.close()
    conn.close()

    return notes

def get_note_by_id(note_id):

    conn = get_db_connection()

    cursor = conn.cursor()

    query = """
    SELECT *
    FROM notes
    WHERE id = %s
    """

    cursor.execute(
        query,
        (note_id,)
    )

    note = cursor.fetchone()

    cursor.close()
    conn.close()

    return note

def update_note_content(note_id,content):

    conn = get_db_connection()

    cursor = conn.cursor()

    query = """
    UPDATE notes
    SET content = %s
    WHERE id = %s
    """

    cursor.execute(
        query,
        (
            content,
            note_id
        )
    )

    conn.commit()

    cursor.close()
    conn.close()