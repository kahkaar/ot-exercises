import tkinter as tk
import tkinter.simpledialog
from dataclasses import dataclass
from pathlib import Path
from tkinter import filedialog, ttk
from typing import Any, Dict, List, Optional, Tuple

from ui.components import MetadataPanel, QueryPanel, ResultsPanel, TablePanel
from services.database import DatabaseService
from services.export import ExportService
from services.query_history import QueryHistoryService


@dataclass
class UIComponents:
    """Component references populated during UI setup."""

    table_panel: Optional[TablePanel] = None
    metadata_panel: Optional[MetadataPanel] = None
    query_panel: Optional[QueryPanel] = None
    results_panel: Optional[ResultsPanel] = None


class UI:
    """Tkinter UI for opening and inspecting a local SQLite database file."""

    def __init__(self, root: tk.Tk) -> None:
        self._root: tk.Tk = root
        self.db_path_var: tk.StringVar = tk.StringVar()
        self.status_var: tk.StringVar = tk.StringVar(
            value="No database opened")
        self.status_label: Optional[ttk.Label] = None
        self._db: Optional[DatabaseService] = None
        self._left_panel: Optional[ttk.Frame] = None
        self._right_panel: Optional[ttk.Frame] = None
        self._components: UIComponents = UIComponents()
        self._create_widgets()

    def _create_widgets(self) -> None:
        frame = ttk.Frame(self._root, padding=12)
        frame.pack(fill=tk.BOTH, expand=True)
        frame.columnconfigure(0, weight=0, minsize=360)
        frame.columnconfigure(1, weight=1)
        frame.rowconfigure(2, weight=1)
        self._create_database_selector(frame)
        self._create_table_panel(frame)
        self._create_metadata_panel()
        self._create_query_panel(frame)
        self._create_results_panel()

    def _create_database_selector(self, frame: ttk.Frame) -> None:
        """Create controls for opening a database file."""

        ttk.Label(frame, text="Selected database:").grid(
            column=0, row=0, sticky=tk.W, padx=(0, 8))

        entry = ttk.Entry(frame, textvariable=self.db_path_var,
                          width=60, state="readonly")
        entry.grid(column=1, row=0, sticky=tk.EW)
        frame.columnconfigure(1, weight=1)

        ttk.Button(frame, text="Open...", command=self.open_database_file).grid(
            column=2, row=0, sticky=tk.E, padx=(8, 0))

        ttk.Button(frame, text="View Schema", command=self.view_full_schema).grid(
            column=2, row=1, sticky=tk.E, padx=(8, 0), pady=(4, 0))

        self.status_label = ttk.Label(
            frame, textvariable=self.status_var, foreground="gray")
        self.status_label.grid(
            column=0, row=1, columnspan=4, sticky=(tk.W), pady=(12, 0))

    def _create_table_panel(self, frame: ttk.Frame) -> None:
        """Create the table list panel."""

        left_panel = ttk.Frame(frame)
        left_panel.grid(column=0, row=2, sticky=tk.NSEW, pady=(16, 0))
        left_panel.columnconfigure(0, weight=1)
        left_panel.rowconfigure(0, weight=1)
        left_panel.rowconfigure(1, weight=1)
        self._left_panel = left_panel
        self._components.table_panel = TablePanel.create(
            parent=left_panel,
            on_select=lambda: self.inspect_selected_table_metadata(
                notify_if_no_selection=False)
        )

    def _create_metadata_panel(self) -> None:
        """Create the table metadata panel."""

        if self._left_panel is None:
            return
        self._components.metadata_panel = MetadataPanel.create(
            self._left_panel)

    def _create_query_panel(self, frame: ttk.Frame) -> None:
        """Create query editor panel on the right side."""

        right_panel = ttk.Frame(frame)
        right_panel.grid(column=1, row=2, columnspan=2, sticky=tk.NSEW,
                         pady=(16, 0), padx=(12, 0))
        right_panel.columnconfigure(0, weight=1)
        right_panel.rowconfigure(0, weight=1)
        right_panel.rowconfigure(1, weight=1)
        self._right_panel = right_panel
        self._components.query_panel = QueryPanel.create(
            right_panel, self.run_select_query, self.show_query_history)

    def _create_results_panel(self) -> None:
        """Create query results panel on the right side."""
        if self._right_panel is None:
            return
        self._components.results_panel = ResultsPanel.create(
            self._right_panel,
            on_export_csv=self._export_results_csv,
            on_export_json=self._export_results_json,
        )

    def _export_results_csv(self):
        columns, rows = self._results_panel().get_export_data()
        if not columns or not rows:
            self._set_status("No results to export.", error=True)
            return
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title="Export results as CSV",
            initialfile="results.csv"
        )
        if not file_path:
            return
        try:
            ExportService.to_csv(columns, rows, file_path)
        except (OSError, ValueError, TypeError) as exc:
            self._set_status(f"Export CSV Error: {exc}", error=True)
            return
        self._set_status(f"Results exported to {file_path}")

    def _export_results_json(self):
        columns, rows = self._results_panel().get_export_data()
        if not columns or not rows:
            self._set_status("No results to export.", error=True)
            return
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Export results as JSON",
            initialfile="results.json"
        )
        if not file_path:
            return
        try:
            ExportService.to_json(columns, rows, file_path)
        except (OSError, ValueError, TypeError) as exc:
            self._set_status(f"Export JSON Error: {exc}", error=True)
            return
        self._set_status(f"Results exported to {file_path}")

    def _table_panel(self) -> TablePanel:
        if self._components.table_panel is None:
            raise RuntimeError("Table panel not initialized.")
        return self._components.table_panel

    def _metadata_panel(self) -> MetadataPanel:
        if self._components.metadata_panel is None:
            raise RuntimeError("Metadata panel not initialized.")
        return self._components.metadata_panel

    def _results_panel(self) -> ResultsPanel:
        if self._components.results_panel is None:
            raise RuntimeError("Results panel not initialized.")
        return self._components.results_panel

    def _query_panel(self) -> QueryPanel:
        if self._components.query_panel is None:
            raise RuntimeError("Query panel not initialized.")
        return self._components.query_panel

    def _update_table_list(self, tables: List[str]) -> None:
        self._table_panel().update_tables(tables)

    def _clear_query_results(self) -> None:
        self._results_panel().clear()

    def _clear_table_metadata(self) -> None:
        self._metadata_panel().clear()

    def _update_table_metadata(
        self,
        metadata: List[Tuple[str, str]] | Dict[str, List[Tuple[str, str]]],
    ) -> None:
        self._metadata_panel().update(metadata)

    def _update_query_results(
        self,
        columns: List[str],
        rows: List[Tuple[Any, ...]],
    ) -> None:
        self._results_panel().update(columns, rows)

    def run_select_query(self) -> None:
        """Run the SELECT query from the text box and display results."""
        if self._db is None:
            self._set_status(
                "Open a database before running a query.", error=True)
            self._clear_query_results()
            return

        query = self._query_panel().query()
        if not query:
            self._set_status("Query is empty.", error=True)
            self._clear_query_results()
            return

        # Save query to history
        QueryHistoryService.save_query(query)

        try:
            columns, rows = self._db.run_select_query(query)
        except ValueError as exc:
            self._set_status(f"Query Error: {exc}", error=True)
            self._clear_query_results()
            return

        self._update_query_results(columns, rows)
        self._set_status(f"Query returned {len(rows)} row(s)")

    def show_query_history(self) -> None:
        """Show a dialog with saved query history."""

        history = QueryHistoryService.load_history()
        if not history:
            self._set_status("No saved queries found.")
            return

        selected = tkinter.simpledialog.askstring(
            "Query History",
            "Select a query by number:\n" +
            "\n".join(f"{i+1}: {q[:60]}" for i, q in enumerate(history)),
            parent=self._root
        )

        if not selected:
            return
        try:
            idx = int(selected) - 1
            if 0 <= idx < len(history):
                self._query_panel().query_text.delete("1.0", tk.END)
                self._query_panel().query_text.insert("1.0", history[idx])
                self._set_status("Loaded query from history.")
            else:
                self._set_status("Invalid selection.", error=True)
        except ValueError:
            self._set_status("Invalid input.", error=True)

    def inspect_selected_table_metadata(
        self,
        notify_if_no_selection: bool = True,
    ) -> None:
        """Inspect metadata for the selected table and display it in the panel."""

        if self._db is None:
            self._set_status(
                "Open a database before inspecting table metadata.", error=True)
            self._clear_table_metadata()
            return

        table_name = self._table_panel().selected_table_name()
        if table_name is None:
            if notify_if_no_selection:
                self._set_status(
                    "Select a table before inspecting metadata.", error=True)
            return

        try:
            metadata = self._db.get_table_metadata(table_name)
        except ValueError as exc:
            self._set_status(f"Metadata Error: {exc}", error=True)
            self._clear_table_metadata()
            return

        self._update_table_metadata(list(metadata))
        self._set_status(f"Showing metadata for table '{table_name}'")

    def view_full_schema(self) -> None:
        """View the full database schema for all tables."""

        if self._db is None:
            self._set_status(
                "Open a database before viewing schema.", error=True)
            self._clear_table_metadata()
            return

        try:
            schema = self._db.get_full_schema()
        except ValueError as exc:
            self._set_status(f"Schema Error: {exc}", error=True)
            self._clear_table_metadata()
            return

        if not schema:
            self._set_status("No tables found in database.")
            self._clear_table_metadata()
            return

        self._update_table_metadata(schema)
        self._set_status(f"Showing full schema ({len(schema)} table(s))")

    def open_database_file(self) -> None:
        """Open a file dialog to select an SQLite database file and validate it."""

        filetypes = [
            ("SQLite files", "*.db *.sqlite *.sqlite3"),
            ("All files", "*.*"),
        ]

        path = filedialog.askopenfilename(
            title="Open SQLite Database", filetypes=filetypes)
        if not path:
            return

        self.db_path_var.set(path)

        db = DatabaseService(path)
        if not db.validate():
            self._set_status(
                "Could not open database: Not a valid SQLite file.", error=True)
            self.db_path_var.set("")
            self._db = None
            self._update_table_list([])
            self._clear_table_metadata()
            return

        self._set_status(f"Opened: {Path(path).name}")
        self._db = db
        self._update_table_list(self._db.list_tables())
        self._clear_table_metadata()
        self._clear_query_results()

    def _set_status(self, message: str, error: bool = False) -> None:
        """Set the status or error message in the status area."""
        self.status_var.set(message)
        if self.status_label:
            self.status_label.configure(foreground="red" if error else "gray")

    def start(self) -> None:
        """Start the Tkinter main loop."""
        self._root.mainloop()
