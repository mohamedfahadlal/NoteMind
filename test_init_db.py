"""Unit tests for NoteMind database schema, initialization, and migration scripts."""

import os
import sys
import unittest
from unittest.mock import MagicMock, patch

# Ensure project root is in sys.path
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from database.init_db import (
    REQUIRED_TABLES,
    DEFAULT_CATEGORIES,
    SCHEMA_FILE,
    drop_tables,
    seed_categories,
    verify_schema,
    init_db
)
from database.migrations import (
    ensure_migrations_table,
    get_applied_migrations,
    get_available_migrations,
    run_migrations,
    show_status
)


class TestSchemaFiles(unittest.TestCase):
    """Test schema.sql and migration file contents."""

    def test_schema_sql_exists(self):
        self.assertTrue(os.path.isfile("schema.sql"))
        self.assertTrue(os.path.isfile("database/schema.sql"))

    def test_schema_contains_all_required_tables(self):
        with open("schema.sql", "r", encoding="utf-8") as f:
            content = f.read()

        for table in REQUIRED_TABLES:
            self.assertIn(f"CREATE TABLE IF NOT EXISTS {table}", content)

        self.assertIn("CREATE TABLE IF NOT EXISTS schema_migrations", content)

    def test_schema_seeds_categories(self):
        with open("schema.sql", "r", encoding="utf-8") as f:
            content = f.read()

        for cat in DEFAULT_CATEGORIES:
            self.assertIn(cat, content)

    def test_initial_migration_exists_and_matches_required_tables(self):
        migration_path = os.path.join("migrations", "001_initial_schema.sql")
        self.assertTrue(os.path.isfile(migration_path))

        with open(migration_path, "r", encoding="utf-8") as f:
            content = f.read()

        for table in REQUIRED_TABLES:
            self.assertIn(f"CREATE TABLE IF NOT EXISTS {table}", content)


class TestMigrations(unittest.TestCase):
    """Test database migration functions with mocked connections."""

    def setUp(self):
        self.mock_conn = MagicMock()
        self.mock_cursor = MagicMock()
        self.mock_conn.cursor.return_value.__enter__.return_value = self.mock_cursor

    def test_ensure_migrations_table(self):
        ensure_migrations_table(self.mock_conn)
        self.mock_cursor.execute.assert_called()
        self.mock_conn.commit.assert_called()

    def test_get_applied_migrations(self):
        self.mock_cursor.fetchall.return_value = [
            {"version": "001_initial_schema.sql"}
        ]
        applied = get_applied_migrations(self.mock_conn)
        self.assertEqual(applied, ["001_initial_schema.sql"])

    def test_get_available_migrations(self):
        migrations = get_available_migrations()
        self.assertIn("001_initial_schema.sql", migrations)

    def test_run_migrations_when_already_applied(self):
        self.mock_cursor.fetchall.return_value = [
            {"version": "001_initial_schema.sql"}
        ]
        applied, success = run_migrations(self.mock_conn)
        self.assertTrue(success)
        self.assertEqual(applied, [])

    def test_run_migrations_when_pending(self):
        self.mock_cursor.fetchall.return_value = []
        applied, success = run_migrations(self.mock_conn)
        self.assertTrue(success)
        self.assertIn("001_initial_schema.sql", applied)
        self.mock_conn.commit.assert_called()

    def test_run_migrations_handles_error(self):
        # Allow ensure_migrations_table, but fail on the migration SQL execution
        def execute_side_effect(sql, *args):
            if "CREATE TABLE IF NOT EXISTS schema_migrations" in sql:
                return
            if "SELECT version FROM schema_migrations" in sql:
                return
            raise Exception("SQL error in migration script")

        self.mock_cursor.fetchall.return_value = []
        self.mock_cursor.execute.side_effect = execute_side_effect
        applied, success = run_migrations(self.mock_conn)
        self.assertFalse(success)
        self.mock_conn.rollback.assert_called()

    def test_show_status(self):
        self.mock_cursor.fetchall.return_value = [
            {"version": "001_initial_schema.sql"}
        ]
        res = show_status(self.mock_conn)
        self.assertTrue(res)


class TestInitDb(unittest.TestCase):
    """Test database initialization functions."""

    def setUp(self):
        self.mock_conn = MagicMock()
        self.mock_cursor = MagicMock()
        self.mock_conn.cursor.return_value.__enter__.return_value = self.mock_cursor

    def test_verify_schema_all_present(self):
        self.mock_cursor.fetchall.return_value = [
            {"table_name": t} for t in REQUIRED_TABLES
        ]
        missing, existing = verify_schema(self.mock_conn)
        self.assertEqual(len(missing), 0)
        self.assertEqual(existing, set(REQUIRED_TABLES))

    def test_verify_schema_detects_missing(self):
        self.mock_cursor.fetchall.return_value = [
            {"table_name": "users"},
            {"table_name": "notes"}
        ]
        missing, existing = verify_schema(self.mock_conn)
        self.assertIn("categories", missing)
        self.assertIn("summaries", missing)
        self.assertNotIn("users", missing)

    def test_drop_tables(self):
        drop_tables(self.mock_conn)
        self.mock_conn.commit.assert_called()
        calls = self.mock_cursor.execute.call_args_list
        dropped = [call[0][0] for call in calls]
        for table in REQUIRED_TABLES:
            self.assertTrue(any(f"DROP TABLE IF EXISTS {table}" in stmt for stmt in dropped))

    def test_seed_categories(self):
        seed_categories(self.mock_conn)
        self.mock_conn.commit.assert_called()
        calls = self.mock_cursor.execute.call_args_list
        seeded = [call[0][1][0] for call in calls if call[0][1]]
        for cat in DEFAULT_CATEGORIES:
            self.assertIn(cat, seeded)

    @patch("database.init_db.create_database_if_not_exists", return_value=True)
    @patch("database.init_db.get_db_connection")
    def test_init_db_success(self, mock_get_conn, mock_create_db):
        mock_get_conn.return_value = self.mock_conn
        # When query for migrations executes, return empty; when verify_schema executes, return all tables
        def fetchall_side_effect():
            return [{"table_name": t, "version": "001_initial_schema.sql"} for t in REQUIRED_TABLES + ["schema_migrations"]]

        self.mock_cursor.fetchall.side_effect = fetchall_side_effect
        success = init_db(drop_first=False, seed=True, use_migrations=True)
        self.assertTrue(success)


class TestFlaskCliIntegration(unittest.TestCase):
    """Test Flask CLI commands are registered in app.py."""

    def test_cli_commands_registered(self):
        # Mock any services dependencies not present in current test environment
        from unittest.mock import MagicMock
        import types
        for mod in ["docx", "PyPDF2", "nltk", "nltk.tokenize", "nltk.corpus", "sklearn",
                    "sklearn.feature_extraction", "sklearn.feature_extraction.text",
                    "sklearn.metrics", "sklearn.metrics.pairwise"]:
            if mod not in sys.modules:
                m = types.ModuleType(mod)
                m.__path__ = []
                m.Document = MagicMock()
                m.PdfReader = MagicMock()
                m.sent_tokenize = MagicMock(return_value=[])
                m.word_tokenize = MagicMock(return_value=[])
                m.stopwords = MagicMock()
                m.TfidfVectorizer = MagicMock()
                m.cosine_similarity = MagicMock()
                sys.modules[mod] = m

        from app import app
        commands = app.cli.list_commands(None)
        self.assertIn("init-db", commands)
        self.assertIn("migrate-db", commands)


if __name__ == "__main__":
    unittest.main()
