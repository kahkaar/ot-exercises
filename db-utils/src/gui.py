import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from services.database import DatabaseService


class UI:
    """Tkinter UI for opening and inspecting a local SQLite database file.

    Args:
        root (tkinter.Tk): The root Tkinter window.
    """

    def __init__(self, root: tk.Tk) -> None:
        self._root = root
        self.db_path_var = tk.StringVar()
        self.status_var = tk.StringVar(value="No database opened")
        self._db = None
        self.query_text = None
        self.results_tree = None
        self._create_widgets()

    def _create_widgets(self) -> None:
        frame = ttk.Frame(self._root, padding=12)
        frame.pack(fill=tk.BOTH, expand=True)
        frame.columnconfigure(1, weight=1)
        frame.rowconfigure(4, weight=1)

        # Database selection
        ttk.Label(frame, text="Selected database:").grid(
            column=0, row=0, sticky=tk.W, padx=(0, 8))

        entry = ttk.Entry(frame, textvariable=self.db_path_var,
                          width=60, state="readonly")
        entry.grid(column=1, row=0, sticky=tk.EW)
        frame.columnconfigure(1, weight=1)

        # Open button
        ttk.Button(frame, text="Open...", command=self.open_database_file).grid(
            column=2, row=0, sticky=tk.E, padx=(8, 0))

        ttk.Label(frame, textvariable=self.status_var, foreground="gray").grid(
            column=0, row=1, columnspan=3, sticky=(tk.W), pady=(12, 0)
        )

        # Table list
        table_frame = ttk.LabelFrame(
            frame, text="Tables", padding=8)
        table_frame.grid(column=0, row=2, columnspan=3,
                         sticky=tk.NSEW, pady=(16, 0))
        self.table_listbox = tk.Listbox(table_frame, height=10, width=40)
        self.table_listbox.pack(fill=tk.BOTH, expand=True)

        query_frame = ttk.LabelFrame(frame, text="Query", padding=8)
        query_frame.grid(column=0, row=3, columnspan=3,
                         sticky=tk.NSEW, pady=(16, 0))
        query_frame.columnconfigure(0, weight=1)
        query_frame.rowconfigure(0, weight=1)

        self.query_text = tk.Text(query_frame, height=6, wrap="none")
        self.query_text.grid(column=0, row=0, sticky=tk.NSEW)

        query_button_frame = ttk.Frame(query_frame)
        query_button_frame.grid(column=0, row=1, sticky=tk.E, pady=(8, 0))
        ttk.Button(query_button_frame, text="Run SELECT",
                   command=self.run_select_query).pack()

        # Results treeview
        results_frame = ttk.LabelFrame(frame, text="Query results", padding=8)
        results_frame.grid(column=0, row=4, columnspan=3,
                           sticky=tk.NSEW, pady=(16, 0))
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)

        results_container = ttk.Frame(results_frame)
        results_container.grid(column=0, row=0, sticky=tk.NSEW)
        results_container.columnconfigure(0, weight=1)
        results_container.rowconfigure(0, weight=1)

        self.results_tree = ttk.Treeview(results_container, show="headings")
        results_tree = self.results_tree
        results_scroll_y = ttk.Scrollbar(
            results_container, orient=tk.VERTICAL, command=results_tree.yview)
        results_scroll_x = ttk.Scrollbar(
            results_container, orient=tk.HORIZONTAL, command=results_tree.xview)
        self.results_tree.configure(
            yscrollcommand=results_scroll_y.set,
            xscrollcommand=results_scroll_x.set,
        )

        self.results_tree.grid(column=0, row=0, sticky=tk.NSEW)
        results_scroll_y.grid(column=1, row=0, sticky=tk.NS)
        results_scroll_x.grid(column=0, row=1, sticky=tk.EW)

    def _update_table_list(self, tables: list[str]) -> None:
        self.table_listbox.delete(0, tk.END)
        for t in tables:
            self.table_listbox.insert(tk.END, t)

    def _clear_query_results(self) -> None:
        if self.results_tree is None:
            return

        self.results_tree.delete(*self.results_tree.get_children())
        self.results_tree["columns"] = ()

    def _update_query_results(
        self,
        columns: list[str],
        rows: list[tuple[object, ...]],
    ) -> None:
        if self.results_tree is None:
            return

        self.results_tree.delete(*self.results_tree.get_children())
        self.results_tree["columns"] = columns

        for column in columns:
            self.results_tree.heading(column, text=column)
            self.results_tree.column(column, width=160, anchor=tk.W)

        for row in rows:
            self.results_tree.insert("", tk.END, values=row)

    def run_select_query(self) -> None:
        """Run te SELECT query from the text box and display results.
        Shows error messages for invalid queries or if no database is opened.
        """
        if self._db is None:
            messagebox.showerror(
                "Query Error", "Open a database before running a query.")
            self.status_var.set("No database opened")
            self._clear_query_results()
            return

        assert self.query_text is not None
        query = self.query_text.get("1.0", tk.END).strip()

        try:
            columns, rows = self._db.run_select_query(query)
        except ValueError as exc:
            messagebox.showerror("Query Error", str(exc))
            self.status_var.set("Query failed")
            self._clear_query_results()
            return

        self._update_query_results(columns, rows)
        self.status_var.set(f"Query returned {len(rows)} row(s)")

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
            return

        self.status_var.set(f"Opened: {Path(path).name}")
        self._db = db
        messagebox.showinfo("Database Opened",
                            f"Successfully opened database:\n{path}")
        self._update_table_list(self._db.list_tables())
        self._clear_query_results()

    def start(self) -> None:
        """Start the Tkinter main loop."""
        self._root.mainloop()
