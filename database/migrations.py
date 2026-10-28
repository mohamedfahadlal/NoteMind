"""Database migration tool for NoteMind.

Discovers and applies SQL migration files in order, keeping track of applied
migrations in the `schema_migrations` table.
"""

import os
import sys

# Ensure project root is in sys.path
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

try:
    from database.connection import get_db_connection
except (ImportError, ModuleNotFoundError):
    try:
        from connection import get_db_connection
    except (ImportError, ModuleNotFoundError):
        get_db_connection = lambda *args, **kwargs: None


MIGRATIONS_DIR = os.path.join(BASE_DIR, "migrations")


def ensure_migrations_table(conn):
    """Ensure the schema_migrations table exists."""
    with conn.cursor() as cur:
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS schema_migrations (
                id SERIAL PRIMARY KEY,
                version VARCHAR(255) UNIQUE NOT NULL,
                applied_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
            );
            """
        )
    conn.commit()


def get_applied_migrations(conn):
    """Retrieve list of already applied migration versions."""
    ensure_migrations_table(conn)
    with conn.cursor() as cur:
        cur.execute("SELECT version FROM schema_migrations ORDER BY id ASC;")
        rows = cur.fetchall()
        applied = []
        for row in rows:
            if isinstance(row, dict) and "version" in row:
                applied.append(row["version"])
            elif hasattr(row, "__getitem__"):
                applied.append(row[0])
        return applied


def get_available_migrations():
    """Discover all SQL migration files sorted alphabetically/numerically."""
    if not os.path.exists(MIGRATIONS_DIR):
        return []
    files = [
        f for f in os.listdir(MIGRATIONS_DIR)
        if f.endswith(".sql") and not f.startswith(".")
    ]
    files.sort()
    return files


def run_migrations(conn=None):
    """Apply all pending migrations in transaction blocks.

    Returns:
        tuple: (applied_list, bool: success)
    """
    close_on_finish = False
    if conn is None:
        conn = get_db_connection()
        if conn is None:
            print("Migration Error: Could not establish database connection.")
            return [], False
        close_on_finish = True

    try:
        ensure_migrations_table(conn)
        applied = set(get_applied_migrations(conn))
        available = get_available_migrations()
        pending = [m for m in available if m not in applied]

        if not pending:
            print("Database is up to date. No pending migrations.")
            return [], True

        print(f"Found {len(pending)} pending migration(s)...")
        newly_applied = []

        for migration_file in pending:
            filepath = os.path.join(MIGRATIONS_DIR, migration_file)
            print(f"  Applying {migration_file}...", end=" ", flush=True)

            with open(filepath, "r", encoding="utf-8") as f:
                sql_content = f.read()

            try:
                with conn.cursor() as cur:
                    # Execute migration SQL script
                    cur.execute(sql_content)
                    # Record version in schema_migrations
                    cur.execute(
                        "INSERT INTO schema_migrations (version) VALUES (%s);",
                        (migration_file,)
                    )
                conn.commit()
                print("DONE")
                newly_applied.append(migration_file)
            except Exception as exc:
                conn.rollback()
                print("FAILED")
                print(f"Error applying migration '{migration_file}': {exc}")
                return newly_applied, False

        print(f"Successfully applied {len(newly_applied)} migration(s).")
        return newly_applied, True

    except Exception as exc:
        if conn:
            conn.rollback()
        print(f"Migration error: {exc}")
        return [], False

    finally:
        if close_on_finish and conn:
            conn.close()


def show_status(conn=None):
    """Display migration status (applied vs pending)."""
    close_on_finish = False
    if conn is None:
        conn = get_db_connection()
        if conn is None:
            print("Error: Could not connect to database.")
            return False
        close_on_finish = True

    try:
        ensure_migrations_table(conn)
        applied = get_applied_migrations(conn)
        applied_set = set(applied)
        available = get_available_migrations()

        print("\n--- Migration Status ---")
        if not available:
            print("No migration files found in migrations/ directory.")
            return True

        for m in available:
            status = "[APPLIED]" if m in applied_set else "[PENDING]"
            print(f" {status} {m}")
        print("------------------------\n")
        return True
    finally:
        if close_on_finish and conn:
            conn.close()


if __name__ == "__main__":
    if "--status" in sys.argv:
        show_status()
    else:
        run_migrations()
