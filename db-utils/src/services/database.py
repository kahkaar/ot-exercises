import sqlite3


class DatabaseService:
    """A class to inspect and validate a local SQLite database file.

    Args:
        path (str): The file path to the SQLite database.
    """

    def __init__(self, path: str) -> None:
        self._path = path

    @property
    def path(self) -> str:
        """Return the path to the database file."""
        return self._path

    def validate(self) -> bool:
        """Validate that the file is a valid SQLite database."""

        try:
            with sqlite3.connect(self._path) as con:
                con.execute("PRAGMA schema_version;")
            return True
        except sqlite3.Error:
            return False

    def list_tables(self) -> list[str]:
        """Return a list of table names in the database."""

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
    ) -> tuple[list[str], list[tuple[object, ...]]]:
        """Run a SELECT query and return column names with rows.

        Args:
            query (str): The SELECT query to execute.
        """

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
