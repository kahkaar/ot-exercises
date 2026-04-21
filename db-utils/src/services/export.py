import csv
import json
from typing import Any, List, Tuple


class ExportService:
    """Export data to file formats."""

    @staticmethod
    def to_csv(columns: List[str], rows: List[Tuple[Any, ...]], file_path: str) -> None:
        """Write rows as CSV."""

        try:
            with open(file_path, "w", encoding="utf-8", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(columns)
                writer.writerows(rows)
        except (OSError, csv.Error) as exc:
            raise RuntimeError(f"Failed to export CSV: {exc}") from exc

    @staticmethod
    def to_json(columns: List[str], rows: List[Tuple[Any, ...]], file_path: str) -> None:
        """Write rows as JSON."""

        try:
            data = [
                {columns[i]: row[i] for i in range(len(columns))}
                for row in rows
            ]
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except (OSError, TypeError, json.JSONDecodeError) as exc:
            raise RuntimeError(f"Failed to export JSON: {exc}") from exc
