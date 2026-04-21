import tkinter as tk
from dataclasses import dataclass
from tkinter import ttk
from typing import Any, Callable, List, Optional, Tuple

from components.tree_panel import create_tree_panel


@dataclass
class ResultsPanel:
    """Panel for query results and export."""

    def __init__(
        self,
        frame: ttk.LabelFrame,
        tree: ttk.Treeview,
        export_csv_btn: Optional[ttk.Button] = None,
        export_json_btn: Optional[ttk.Button] = None
    ) -> None:
        self.frame: ttk.LabelFrame = frame
        self.tree: ttk.Treeview = tree
        self.export_csv_btn: Optional[ttk.Button] = export_csv_btn
        self.export_json_btn: Optional[ttk.Button] = export_json_btn
        self._columns: List[str] = []
        self._rows: List[Tuple[Any, ...]] = []

    @classmethod
    def create(
        cls,
        parent: tk.Widget,
        on_export_csv: Optional[Callable[[], None]] = None,
        on_export_json: Optional[Callable[[], None]] = None
    ) -> "ResultsPanel":
        """Create results panel widgets."""
        frame, tree = create_tree_panel(parent, "Query results")
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(column=0, row=1, sticky=tk.E, padx=8, pady=(0, 8))
        export_csv_btn = ttk.Button(
            btn_frame,
            text="Export CSV",
            command=on_export_csv if on_export_csv else (lambda: None)
        )
        export_csv_btn.grid(column=0, row=0, padx=(0, 8))
        export_json_btn = ttk.Button(
            btn_frame,
            text="Export JSON",
            command=on_export_json if on_export_json else (lambda: None)
        )
        export_json_btn.grid(column=1, row=0)
        return cls(
            frame=frame,
            tree=tree,
            export_csv_btn=export_csv_btn,
            export_json_btn=export_json_btn
        )

    def clear(self) -> None:
        """Clear all rows and columns."""
        self.tree.delete(*self.tree.get_children())
        self.tree["columns"] = ()
        self._columns = []
        self._rows = []

    def update(self, columns: List[str], rows: List[Tuple[Any, ...]]) -> None:
        """Update tree with query results."""
        self.clear()
        self._columns = columns.copy()
        self._rows = rows.copy()
        self.tree["columns"] = tuple(columns)

        for column in columns:
            self.tree.heading(column, text=column)
            self.tree.column(
                column,
                width=160,
                minwidth=160,
                anchor=tk.W,
                stretch=False,
            )

        if columns:
            last_column = columns[-1]
            self.tree.column(last_column, stretch=False, minwidth=160)

        for row in rows:
            self.tree.insert("", tk.END, values=row)

    def get_export_data(self) -> Tuple[List[str], List[Tuple[Any, ...]]]:
        """Get columns and rows for export."""
        return self._columns, self._rows
