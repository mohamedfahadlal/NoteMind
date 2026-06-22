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
