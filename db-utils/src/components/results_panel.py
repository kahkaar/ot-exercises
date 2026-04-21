# pylint: disable=duplicate-code
# Why: duplicate-code error with query_panel.py imports.
# Justification: The components are using similar imports,
# have different purposes and implementations.
# Creating a shared imports module would add
# unnecessary complexity and coupling between the components.

import tkinter as tk
from dataclasses import dataclass
from tkinter import ttk
from typing import Callable

from components.tree_panel import create_tree_panel


@dataclass
class ResultsPanel:
    """Query results panel component with export support."""

    def __init__(
        self,
        frame: ttk.LabelFrame,
        tree: ttk.Treeview,
        export_csv_btn: ttk.Button | None = None,
        export_json_btn: ttk.Button | None = None
    ) -> None:
        self.frame = frame
        self.tree = tree
        self.export_csv_btn = export_csv_btn
        self.export_json_btn = export_json_btn
        self._columns = []
        self._rows = []

    @classmethod
    def create(
        cls,
        parent: tk.Widget,
        on_export_csv: Callable[[], None] | None = None,
        on_export_json: Callable[[], None] | None = None
    ) -> "ResultsPanel":
        """Create and place the query results widgets with export buttons."""
        frame, tree = create_tree_panel(parent, "Query results")

        # Export buttons
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
        """Clear rows and columns from the results tree and reset export data."""
        self.tree.delete(*self.tree.get_children())
        self.tree["columns"] = ()
        self._columns = []
        self._rows = []

    def update(self, columns: list[str], rows: list[tuple[object, ...]]) -> None:
        """Render query result columns and rows in the tree and store for export."""
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

    def get_export_data(self) -> tuple[list[str], list[tuple[object, ...]]]:
        return self._columns, self._rows
