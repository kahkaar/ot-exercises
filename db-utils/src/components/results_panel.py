import tkinter as tk
from dataclasses import dataclass
from tkinter import ttk

from components.tree_panel import create_tree_panel


@dataclass
class ResultsPanel:
    """Query results panel component."""

    frame: ttk.LabelFrame
    tree: ttk.Treeview

    @classmethod
    def create(cls, parent: tk.Widget) -> "ResultsPanel":
        """Create and place the query results widgets."""
        frame, tree = create_tree_panel(parent, "Query results")

        return cls(frame=frame, tree=tree)

    def clear(self) -> None:
        """Clear rows and columns from the results tree."""
        self.tree.delete(*self.tree.get_children())
        self.tree["columns"] = ()

    def update(self, columns: list[str], rows: list[tuple[object, ...]]) -> None:
        """Render query result columns and rows in the tree."""
        self.clear()
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
