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
def get_tag_by_name(tag_name):

    conn = get_db_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id
        FROM tags
        WHERE tag_name = %s
        """,
        (tag_name,)
    )

    tag = cursor.fetchone()

    cursor.close()
    conn.close()

    return tag
def create_tag(tag_name):

    conn = get_db_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO tags(tag_name)
        VALUES(%s)
        ON CONFLICT(tag_name)
        DO NOTHING
        """,
        (tag_name,)
    )

    conn.commit()

    cursor.close()
    conn.close()

def assign_tag(note_id, tag_id):

    conn = get_db_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO note_tags
        (
            note_id,
            tag_id
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
            tag_id
        )
    )

    conn.commit()

    cursor.close()
    conn.close()


def get_note_tags(note_id):

    conn = get_db_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT t.tag_name
        FROM tags t
        JOIN note_tags nt
            ON t.id = nt.tag_id
        WHERE nt.note_id = %s
        """,
        (note_id,)
    )

    tags = cursor.fetchall()

    cursor.close()
    conn.close()

    return tags

def search_notes(user_id, query):

    conn = get_db_connection()

    cursor = conn.cursor()

    sql = """
    SELECT *
    FROM notes
    WHERE user_id = %s
    AND (
        LOWER(title) LIKE LOWER(%s)
        OR LOWER(content) LIKE LOWER(%s)
    )
    ORDER BY uploaded_at DESC
    """

    search = f"%{query}%"

    cursor.execute(
        sql,
        (
            user_id,
            search,
            search
        )
    )

    notes = cursor.fetchall()

    cursor.close()
    conn.close()

    return notes
