import os
import sqlite3
from typing import List, Optional


class QueryHistoryService:
    """Service for saving and loading query history to a local SQLite database."""

    DEFAULT_DB_PATH = os.path.expanduser("~/.db_utils.sqlite3")

    @classmethod
    def _ensure_table(cls, db_path: Optional[str] = None) -> None:
        """Ensure the history table exists."""
        db_path = db_path or cls.DEFAULT_DB_PATH
        with sqlite3.connect(db_path) as con:
            con.execute(
                """
                CREATE TABLE IF NOT EXISTS query_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    query TEXT NOT NULL UNIQUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

    @classmethod
    def save_query(cls, query: str, db_path: Optional[str] = None) -> None:
        """Save a query to the history database."""
        if not query.strip():
            return
        db_path = db_path or cls.DEFAULT_DB_PATH
        cls._ensure_table(db_path)
        try:
            with sqlite3.connect(db_path) as con:
                con.execute(
                    "INSERT OR IGNORE INTO query_history (query) VALUES (?)",
                    (query.strip(),)
                )
        except sqlite3.DatabaseError:
            pass

    @classmethod
    def load_history(cls, db_path: Optional[str] = None) -> List[str]:
        """Load query history from the history database."""
        db_path = db_path or cls.DEFAULT_DB_PATH
        cls._ensure_table(db_path)
        try:
            with sqlite3.connect(db_path) as con:
                cur = con.execute(
                    "SELECT query FROM query_history ORDER BY id DESC"
                )
                return [row[0] for row in cur.fetchall()]
        except sqlite3.DatabaseError:
            return []
