import psycopg2

try:
    conn = psycopg2.connect(
        dbname="notemind",
        user="notemind_user",
        password="notemind123",
        host="localhost",
        port="5432"
    )

    print("Database Connected Successfully!")

    conn.close()

except Exception as e:
    print("Connection Failed")
    print(e)