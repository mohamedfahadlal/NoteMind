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

def assign_category(
    note_id,
    category_id
):

    conn = get_db_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO note_categories
        (
            note_id,
            category_id
        )
        VALUES
        (
            %s,
            %s
        )
        ON CONFLICT DO NOTHING
        """,
        (
            note_id,
            category_id
        )
    )

    conn.commit()

    cursor.close()
    conn.close()
def get_category_id_by_name(
    category_name
):

    conn = get_db_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id
        FROM categories
        WHERE name = %s
        """,
        (
            category_name,
        )
    )

    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return result


def get_note_category(note_id):

    conn = get_db_connection()

    cursor = conn.cursor()

    query = """
    SELECT c.name
    FROM categories c
    JOIN note_categories nc
        ON c.id = nc.category_id
    WHERE nc.note_id = %s
    """

    cursor.execute(
        query,
        (note_id,)
    )

    category = cursor.fetchone()

    cursor.close()
    conn.close()

    return category