import psycopg2
from psycopg2.extras import RealDictCursor

from config import *

def get_db_connection():

    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
            cursor_factory=RealDictCursor
        )

        return conn

    except Exception as e:
        print(e)
        return None