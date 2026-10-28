try:
    import psycopg2
    from psycopg2.extras import RealDictCursor
    PSYCOPG2_AVAILABLE = True
except ImportError:
    psycopg2 = None
    RealDictCursor = None
    PSYCOPG2_AVAILABLE = False

try:
    from config import (
        DB_NAME,
        DB_USER,
        DB_PASSWORD,
        DB_HOST,
        DB_PORT
    )
except ImportError:
    from database.config import (
        DB_NAME,
        DB_USER,
        DB_PASSWORD,
        DB_HOST,
        DB_PORT
    )

def get_db_connection(dbname=None):
    if not PSYCOPG2_AVAILABLE:
        print("Database error: psycopg2 is not available. Please install dependencies from requirements.txt.")
        return None

    target_db = dbname if dbname is not None else DB_NAME
    try:
        conn = psycopg2.connect(
            dbname=target_db,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
            cursor_factory=RealDictCursor
        )
        return conn
    except Exception as e:
        print(f"Database connection error ({target_db}): {e}")
        return None
