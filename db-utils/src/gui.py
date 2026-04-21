import tkinter as tk
from dataclasses import dataclass
from pathlib import Path
from tkinter import filedialog, messagebox, ttk
from typing import Any, List, Optional, Tuple

from components import MetadataPanel, QueryPanel, ResultsPanel, TablePanel
from services.database import DatabaseService
from services.export import ExportService


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

        ttk.Label(frame, textvariable=self.status_var, foreground="gray").grid(
            column=0, row=1, columnspan=3, sticky=(tk.W), pady=(12, 0)
        )

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
            right_panel, self.run_select_query)

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
            messagebox.showinfo("Export CSV", "No results to export.")
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
            messagebox.showerror("Export CSV Error", str(exc))
            return
        messagebox.showinfo("Export CSV", f"Results exported to {file_path}")

    def _export_results_json(self):
        columns, rows = self._results_panel().get_export_data()
        if not columns or not rows:
            messagebox.showinfo("Export JSON", "No results to export.")
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
            messagebox.showerror("Export JSON Error", str(exc))
            return
        messagebox.showinfo("Export JSON", f"Results exported to {file_path}")

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
        metadata: List[Tuple[str, str]],
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
            messagebox.showerror(
                "Query Error", "Open a database before running a query.")
            self.status_var.set("No database opened")
            self._clear_query_results()
            return

        query = self._query_panel().query()

        try:
            columns, rows = self._db.run_select_query(query)
        except ValueError as exc:
            messagebox.showerror("Query Error", str(exc))
            self.status_var.set("Query failed")
            self._clear_query_results()
            return

        self._update_query_results(columns, rows)
        self.status_var.set(f"Query returned {len(rows)} row(s)")

    def inspect_selected_table_metadata(
        self,
        notify_if_no_selection: bool = True,
    ) -> None:
        """Inspect metadata for the selected table and display it in the panel."""

        if self._db is None:
            messagebox.showerror(
                "Metadata Error", "Open a database before inspecting table metadata.")
            self.status_var.set("No database opened")
            self._clear_table_metadata()
            return

        table_name = self._table_panel().selected_table_name()
        if table_name is None:
            if notify_if_no_selection:
                messagebox.showerror(
                    "Metadata Error", "Select a table before inspecting metadata.")
            return

        try:
            metadata = self._db.get_table_metadata(table_name)
        except ValueError as exc:
            messagebox.showerror("Metadata Error", str(exc))
            self.status_var.set("Metadata inspection failed")
            self._clear_table_metadata()
            return

        self._update_table_metadata(list(metadata))
        self.status_var.set(f"Showing metadata for table '{table_name}'")

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
            messagebox.showerror(
                "Database Error", "Could not open database: Not a valid SQLite file.")
            self.status_var.set("Failed to open database")
            self.db_path_var.set("")
            self._db = None
            self._update_table_list([])
            self._clear_table_metadata()
            return

        self.status_var.set(f"Opened: {Path(path).name}")
        self._db = db
        messagebox.showinfo("Database Opened",
                            f"Successfully opened database:\n{path}")
        self._update_table_list(self._db.list_tables())
        self._clear_table_metadata()
        self._clear_query_results()

    def start(self) -> None:
        """Start the Tkinter main loop."""
        self._root.mainloop()
