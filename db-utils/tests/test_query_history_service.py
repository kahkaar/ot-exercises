import os
import sqlite3
import tempfile
import unittest

from src.services.query_history import QueryHistoryService


class TestQueryHistoryService(unittest.TestCase):
    """Unit tests for the QueryHistoryService class."""

    def setUp(self) -> None:
        fd, self.db_path = tempfile.mkstemp(suffix=".sqlite3")
        os.close(fd)
        # Remove file so QueryHistoryService creates it
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def tearDown(self) -> None:
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_save_and_load_single_query(self):
        """Test saving and loading a single query."""

        QueryHistoryService.save_query("SELECT 1", self.db_path)
        history = QueryHistoryService.load_history(self.db_path)
        self.assertIn("SELECT 1", history)

    def test_save_duplicate_query(self):
        """Test that duplicate queries are not saved twice."""

        QueryHistoryService.save_query("SELECT 2", self.db_path)
        QueryHistoryService.save_query("SELECT 2", self.db_path)
        history = QueryHistoryService.load_history(self.db_path)
        self.assertEqual(history.count("SELECT 2"), 1)

    def test_save_empty_query(self):
        """Test that empty queries are not saved."""

        QueryHistoryService.save_query("   ", self.db_path)
        history = QueryHistoryService.load_history(self.db_path)
        self.assertEqual(history, [])

    def test_load_history_empty(self):
        """Test loading history from a new database returns an empty list."""

        history = QueryHistoryService.load_history(self.db_path)
        self.assertEqual(history, [])

    def test_history_order(self):
        """Test that queries are returned in reverse insertion order (most recent first)."""

        QueryHistoryService.save_query("SELECT 1", self.db_path)
        QueryHistoryService.save_query("SELECT 2", self.db_path)
        QueryHistoryService.save_query("SELECT 3", self.db_path)
        history = QueryHistoryService.load_history(self.db_path)
        self.assertEqual(history[0], "SELECT 3")
        self.assertEqual(history[1], "SELECT 2")
        self.assertEqual(history[2], "SELECT 1")
