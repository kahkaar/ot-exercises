import sqlite3
from typing import List


class DatabaseService:
    """A class to inspect and validate a local SQLite database file."""

    def __init__(self, db_path: str) -> None:
        self.db_path = db_path

    def validate(self) -> bool:
        """Validate that the file is a valid SQLite database."""

        try:
            with sqlite3.connect(self.db_path) as con:
                con.execute("PRAGMA schema_version;")
            return True
        except sqlite3.Error:
            return False

    def list_tables(self) -> List[str]:
        """Return a list of table names in the database."""

        query = """
            SELECT name
            FROM sqlite_master
            WHERE type='table' AND name NOT LIKE 'sqlite_%'
            ORDER BY name;
        """

        try:
            with sqlite3.connect(self.db_path) as con:
                cur = con.execute(query)
            return [row[0] for row in cur.fetchall()]
        except sqlite3.Error:
            return []
