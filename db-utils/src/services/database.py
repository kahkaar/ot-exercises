import sqlite3
from typing import Any, List, Tuple


class DatabaseService:
    """Inspect and validate a SQLite database file."""

    def __init__(self, path: str) -> None:
        self._path = path

    @property
    def path(self) -> str:
        """Get database file path."""
        return self._path

    def validate(self) -> bool:
        """Check if file is a valid SQLite database."""

        try:
            with sqlite3.connect(self._path) as con:
                con.execute("PRAGMA schema_version;")
            return True
        except sqlite3.Error:
            return False

    def list_tables(self) -> List[str]:
        """List table names in the database."""

        query = """
            SELECT name
            FROM sqlite_master
            WHERE type='table' AND name NOT LIKE 'sqlite_%'
            ORDER BY name;
        """

        try:
            with sqlite3.connect(self._path) as con:
                cur = con.execute(query)
            return [row[0] for row in cur.fetchall()]
        except sqlite3.Error:
            return []

    def run_select_query(
        self,
        query: str,
    ) -> Tuple[List[str], List[Tuple[Any, ...]]]:
        """Run a SELECT query and return columns and rows."""

        normalized_query = query.strip()
        if not normalized_query:
            raise ValueError("Query cannot be empty.")
        if not normalized_query.lower().startswith("select"):
            raise ValueError("Only SELECT queries are supported.")

        try:
            with sqlite3.connect(self._path) as con:
                cur = con.execute(normalized_query)
                cols = [desc[0] for desc in cur.description or []]
                rows = [tuple(row) for row in cur.fetchall()]
            return cols, rows
        except sqlite3.Error as exc:
            raise ValueError(f"Could not execute query: {exc}") from exc

    def get_table_metadata(self, table_name: str) -> List[Tuple[str, str]]:
        """Get column metadata (name, type) for a table."""

        normalized_table_name = table_name.strip()
        if not normalized_table_name:
            raise ValueError("Table name cannot be empty.")

        exists_query = """
            SELECT 1
            FROM sqlite_master
            WHERE type='table' AND name = ?
            LIMIT 1;
        """

        escaped_table_name = normalized_table_name.replace('"', '""')
        metadata_query = f'PRAGMA table_info("{escaped_table_name}");'

        try:
            with sqlite3.connect(self._path) as con:
                exists = con.execute(
                    exists_query, (normalized_table_name,)).fetchone()
                if exists is None:
                    raise ValueError(
                        f"Table '{normalized_table_name}' does not exist.")

                rows = con.execute(metadata_query).fetchall()
            return [(str(row[1]), str(row[2] or "")) for row in rows]
        except sqlite3.Error as exc:
            raise ValueError(
                f"Could not inspect table metadata: {exc}") from exc
