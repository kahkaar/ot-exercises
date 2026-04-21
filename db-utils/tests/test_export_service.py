import csv
import json
import os
import tempfile
import unittest

from src.services.export import ExportService


class TestExportService(unittest.TestCase):
    """Unit tests for the ExportService class."""

    def setUp(self) -> None:
        self.fields = ["id", "name", "value"]
        self.records = [
            (1, "Ada Lovelace", 10.5),
            (2, "Alan Turing", 20.0),
            (3, "Grace Hopper", 30.25),
        ]
        self.temp_dir = tempfile.TemporaryDirectory()
        self.csv_path = os.path.join(self.temp_dir.name, "test.csv")
        self.json_path = os.path.join(self.temp_dir.name, "test.json")

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_to_csv(self) -> None:
        """Test that to_csv writes the correct CSV file."""

        ExportService.to_csv(self.fields, self.records, self.csv_path)
        with open(self.csv_path, newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            csv_content = list(reader)
        self.assertEqual(csv_content[0], self.fields)
        self.assertEqual(csv_content[1:], [[str(cell)
                         for cell in record] for record in self.records])

    def test_to_json(self) -> None:
        """Test that to_json writes the correct JSON file."""

        ExportService.to_json(self.fields, self.records, self.json_path)
        with open(self.json_path, encoding="utf-8") as f:
            data = json.load(f)
        self.assertIsInstance(data, list)
        self.assertEqual(data, [dict(zip(self.fields, record))
                         for record in self.records])

    def test_to_csv_invalid_path(self) -> None:
        """Test to_csv raises RuntimeError on invalid file path."""

        with self.assertRaises(RuntimeError):
            ExportService.to_csv(self.fields, self.records,
                                 "/invalid_path/test.csv")

    def test_to_json_invalid_path(self) -> None:
        """Test to_json raises RuntimeError on invalid file path."""

        with self.assertRaises(RuntimeError):
            ExportService.to_json(self.fields, self.records,
                                  "/invalid_path/test.json")

    def test_to_json_invalid_data(self) -> None:
        """Test to_json raises RuntimeError on unserializable data."""

        class Unserializable:
            pass
        bad_records = [(Unserializable(),)]
        with self.assertRaises(RuntimeError):
            ExportService.to_json(["bad"], bad_records, self.json_path)


if __name__ == "__main__":
    unittest.main()
