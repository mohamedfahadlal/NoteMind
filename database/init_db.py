"""Database initialization script for NoteMind.

Sets up all required database tables, indexes, and initial seed data for new
or existing environments.
"""

import os
import sys
import argparse

# Ensure project root is in sys.path
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

try:
    from config import (
        DB_NAME,
        DB_USER,
        DB_PASSWORD,
        DB_HOST,
        DB_PORT
    )
except (ImportError, ModuleNotFoundError):
    from database.config import (
        DB_NAME,
        DB_USER,
        DB_PASSWORD,
        DB_HOST,
        DB_PORT
    )

try:
    from database.connection import get_db_connection
except (ImportError, ModuleNotFoundError):
    try:
        from connection import get_db_connection
    except (ImportError, ModuleNotFoundError):
        get_db_connection = lambda *args, **kwargs: None

try:
    from database.migrations import run_migrations, ensure_migrations_table
except (ImportError, ModuleNotFoundError):
    try:
        from migrations import run_migrations, ensure_migrations_table
    except (ImportError, ModuleNotFoundError):
        run_migrations = None
        ensure_migrations_table = None


SCHEMA_FILE = os.path.join(os.path.dirname(__file__), "schema.sql")
if not os.path.exists(SCHEMA_FILE):
    SCHEMA_FILE = os.path.join(BASE_DIR, "schema.sql")

REQUIRED_TABLES = [
    "users",
    "notes",
    "categories",
    "note_categories",
    "tags",
    "note_tags",
    "summaries",
    "search_history",
    "note_views"
]

DEFAULT_CATEGORIES = [
    "DBMS",
    "Operating Systems",
    "Computer Networks",
    "Machine Learning",
    "Data Structures"
]


def create_database_if_not_exists():
    """Attempt to create the target PostgreSQL database if it does not already exist."""
    try:
        import psycopg2
        from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
    except (ImportError, ModuleNotFoundError):
        print("Note: psycopg2 is not installed or available.")
        return False

    # First test if target database is already accessible
    test_conn = get_db_connection()
    if test_conn:
        test_conn.close()
        return True

    # Try connecting to default postgres maintenance database
    maintenance_dbs = ["postgres", "template1"]
    for mdb in maintenance_dbs:
        try:
            admin_conn = psycopg2.connect(
                dbname=mdb,
                user=DB_USER,
                password=DB_PASSWORD,
                host=DB_HOST,
                port=DB_PORT
            )
            admin_conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            with admin_conn.cursor() as cur:
                cur.execute(
                    "SELECT 1 FROM pg_database WHERE datname = %s;",
                    (DB_NAME,)
                )
                exists = cur.fetchone()
                if not exists:
                    print(f"Database '{DB_NAME}' does not exist. Creating it now...")
                    # Note: database name in CREATE DATABASE cannot use parametrized placeholder
                    cur.execute(f'CREATE DATABASE "{DB_NAME}";')
                    print(f"Database '{DB_NAME}' created successfully.")
                admin_conn.close()
                return True
        except Exception:
            continue

    print(f"Note: Could not automatically verify or create database '{DB_NAME}'.")
    print(f"If the database does not exist, run in PostgreSQL:")
    print(f"  CREATE DATABASE {DB_NAME};")
    return False


def drop_tables(conn):
    """Drop all NoteMind application tables and constraints."""
    print("Dropping existing application tables...")
    tables_to_drop = [
        "schema_migrations",
        "note_views",
        "search_history",
        "summaries",
        "note_tags",
        "tags",
        "note_categories",
        "categories",
        "notes",
        "users"
    ]
    with conn.cursor() as cur:
        for table in tables_to_drop:
            cur.execute(f"DROP TABLE IF EXISTS {table} CASCADE;")
    conn.commit()
    print("All tables dropped successfully.")


def seed_categories(conn):
    """Seed initial categories if they do not already exist."""
    with conn.cursor() as cur:
        for category in DEFAULT_CATEGORIES:
            cur.execute(
                """
                INSERT INTO categories (name)
                VALUES (%s)
                ON CONFLICT (name) DO NOTHING;
                """,
                (category,)
            )
    conn.commit()
    print(f"Seeded {len(DEFAULT_CATEGORIES)} default categories.")


def get_existing_tables(conn):
    """Return a set of table names in the public schema."""
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public';
            """
        )
        rows = cur.fetchall()
        tables = set()
        for row in rows:
            if isinstance(row, dict) and "table_name" in row:
                tables.add(row["table_name"])
            elif hasattr(row, "__getitem__"):
                tables.add(row[0])
        return tables


def verify_schema(conn):
    """Verify that all required tables exist in the database."""
    existing = get_existing_tables(conn)
    missing = [t for t in REQUIRED_TABLES if t not in existing]
    return missing, existing


def init_db(drop_first=False, seed=True, use_migrations=True):
    """Initialize database schema, tables, and default seed data.

    Args:
        drop_first (bool): If True, drops existing tables before recreating.
        seed (bool): If True, seeds default categories.
        use_migrations (bool): If True, synchronizes with the migration tool.

    Returns:
        bool: True if initialization succeeded, False otherwise.
    """
    print(f"=== Initializing NoteMind Database: '{DB_NAME}' ===")
    create_database_if_not_exists()

    conn = get_db_connection()
    if conn is None:
        print(f"Error: Unable to connect to database '{DB_NAME}' at {DB_HOST}:{DB_PORT}.")
        print("Please check your database server, username, password, and port in config.py or .env.")
        return False

    try:
        if drop_first:
            drop_tables(conn)

        # 1. Apply schema from schema.sql
        if os.path.exists(SCHEMA_FILE):
            print(f"Applying schema definition from {SCHEMA_FILE}...")
            with open(SCHEMA_FILE, "r", encoding="utf-8") as f:
                schema_sql = f.read()
            with conn.cursor() as cur:
                cur.execute(schema_sql)
            conn.commit()
            print("Schema SQL applied successfully.")
        else:
            print(f"Warning: {SCHEMA_FILE} not found.")

        # 2. Synchronize with migrations
        if use_migrations and run_migrations:
            ensure_migrations_table(conn)
            run_migrations(conn)

        # 3. Seed default categories
        if seed:
            seed_categories(conn)

        # 4. Verify all required tables exist
        missing, existing = verify_schema(conn)
        if missing:
            print(f"Warning: Some required tables are missing: {', '.join(missing)}")
            return False

        print("\nAll required tables verified:")
        for t in REQUIRED_TABLES:
            print(f"  [OK] Table: {t}")

        print("\n=== NoteMind Database Initialized Successfully! ===\n")
        return True

    except Exception as exc:
        conn.rollback()
        print(f"\nDatabase initialization failed: {exc}")
        return False
    finally:
        conn.close()


def main():
    parser = argparse.ArgumentParser(
        description="Initialize NoteMind PostgreSQL database and tables."
    )
    parser.add_argument(
        "--drop",
        "--reset",
        action="store_true",
        help="Drop existing tables before recreating (WARNING: removes all data)."
    )
    parser.add_argument(
        "--seed",
        action="store_true",
        help="Seed default categories only."
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Check and verify database connection and required tables without modifying schema."
    )
    parser.add_argument(
        "--migrate",
        action="store_true",
        help="Run pending migrations using the migration tool."
    )

    args = parser.parse_args()

    if args.check:
        conn = get_db_connection()
        if not conn:
            print(f"Failed to connect to database '{DB_NAME}'.")
            sys.exit(1)
        missing, existing = verify_schema(conn)
        conn.close()
        if missing:
            print(f"Missing tables: {', '.join(missing)}")
            sys.exit(1)
        else:
            print(f"All {len(REQUIRED_TABLES)} required tables are present in '{DB_NAME}'.")
            sys.exit(0)

    if args.migrate:
        if run_migrations:
            success = run_migrations()[1]
            sys.exit(0 if success else 1)
        else:
            print("Migration module not available.")
            sys.exit(1)

    if args.seed:
        conn = get_db_connection()
        if not conn:
            print(f"Failed to connect to database '{DB_NAME}'.")
            sys.exit(1)
        seed_categories(conn)
        conn.close()
        sys.exit(0)

    success = init_db(drop_first=args.drop)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
