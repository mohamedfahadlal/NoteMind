from connection import get_db_connection

conn = get_db_connection()

if conn:
    print("Database Connected Successfully!")
    conn.close()
else:
    print("Database Connection Failed!")
