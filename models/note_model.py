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

    conn.commit()

    cursor.close()
    conn.close()

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
