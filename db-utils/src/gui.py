import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from services.database import DatabaseService


class UI:
    """Tkinter UI for opening and inspecting a local SQLite database file."""

    def __init__(self, root: tk.Tk) -> None:
        self._root = root
        self.db_path_var = tk.StringVar()
        self.status_var = tk.StringVar(value="No database opened")
        self.table_list_var = tk.StringVar(value="")
        self._db = None
        self._create_widgets()

    def _create_widgets(self) -> None:
        frame = ttk.Frame(self._root, padding=12)
        frame.pack(fill=tk.BOTH, expand=True)

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

    def _update_table_list(self, tables: list[str]) -> None:
        self.table_listbox.delete(0, tk.END)
        for t in tables:
            self.table_listbox.insert(tk.END, t)

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

    def start(self) -> None:
        """Start the Tkinter main loop."""
        self._root.mainloop()
