import os
import json
import csv
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
        ExportService.to_csv(self.fields, self.records, self.csv_path)
        with open(self.csv_path, newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            csv_content = list(reader)
        self.assertEqual(csv_content[0], self.fields)
        self.assertEqual(csv_content[1:], [[str(cell)
                         for cell in record] for record in self.records])

    def test_to_json(self) -> None:
        ExportService.to_json(self.fields, self.records, self.json_path)
        with open(self.json_path, encoding="utf-8") as f:
            data = json.load(f)
        self.assertIsInstance(data, list)
        self.assertEqual(data, [dict(zip(self.fields, record))
                         for record in self.records])


if __name__ == "__main__":
    unittest.main()
