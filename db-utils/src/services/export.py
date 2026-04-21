import csv
import json


class ExportService:
    @staticmethod
    def to_csv(columns: list[str], rows: list[tuple[object, ...]], file_path: str) -> None:
        """Export rows to a CSV file."""
        with open(file_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(columns)
            writer.writerows(rows)

    @staticmethod
    def to_json(columns: list[str], rows: list[tuple[object, ...]], file_path: str) -> None:
        """Export rows to a JSON file."""
        # Adding typing to the data variable for pylance to recognize the structure of the data list
        data: list[dict[str, object]] = []
        for row in rows:
            item = {columns[i]: row[i] for i in range(len(columns))}
            data.append(item)
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
