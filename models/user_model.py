from database.connection import get_db_connection


def create_user(
    name,
    email,
    password_hash
):
    conn = get_db_connection()

    cursor = conn.cursor()

    query = """
    INSERT INTO users
    (
        name,
        email,
        password_hash
    )
    VALUES
    (
        %s,
        %s,
        %s
    )
    """

    cursor.execute(
        query,
        (
            name,
            email,
            password_hash
        )
    )

    conn.commit()

    cursor.close()
    conn.close()

def get_user_by_email(email):

    conn = get_db_connection()

    cursor = conn.cursor()

    query = """
    SELECT *
    FROM users
    WHERE email = %s
    """

    cursor.execute(query, (email,))

    user = cursor.fetchone()

    cursor.close()
    conn.close()

    return user
