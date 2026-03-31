import os
import sqlite3
import tempfile
import unittest

from src.services.database import DatabaseService


def _create_test_db(path: str, tables: list[str] | None = None) -> None:
    tables = tables or []
    with sqlite3.connect(path) as con:
        for t in tables:
            con.execute(f"CREATE TABLE {t} (id INTEGER PRIMARY KEY);")


class TestDatabaseService(unittest.TestCase):
    """Unit tests for the DatabaseService class."""

    def setUp(self) -> None:
        fd, self.db_path = tempfile.mkstemp(suffix=".db")
        os.close(fd)

    def tearDown(self) -> None:
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_validate_valid_db(self) -> None:
        """Test that validate() returns True for a valid SQLite database."""

        _create_test_db(self.db_path, ["foo"])
        db = DatabaseService(self.db_path)
        self.assertTrue(db.validate())

    def test_validate_invalid_db(self) -> None:
        """Test that validate() returns False for an invalid SQLite database."""

        with open(self.db_path, "w", encoding="utf-8") as f:
            f.write("not a db")
        db = DatabaseService(self.db_path)
        self.assertFalse(db.validate())

    def test_list_tables_returns_tables(self) -> None:
        """Test that list_tables() returns the correct list of tables."""

        _create_test_db(self.db_path, ["foo", "bar"])
        db = DatabaseService(self.db_path)
        tables = db.list_tables()
        self.assertEqual(set(tables), {"foo", "bar"})

    def test_list_tables_empty(self) -> None:
        """Test that list_tables() returns an empty list when there are no tables."""

        _create_test_db(self.db_path, [])
        db = DatabaseService(self.db_path)
        self.assertEqual(db.list_tables(), [])

    def test_list_tables_invalid_db(self) -> None:
        """Test that list_tables() returns an empty list for an invalid database."""

        with open(self.db_path, "w", encoding="utf-8") as f:
            f.write("not a db")
        db = DatabaseService(self.db_path)
        self.assertEqual(db.list_tables(), [])


if __name__ == "__main__":
    unittest.main()
