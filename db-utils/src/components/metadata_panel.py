import tkinter as tk
from dataclasses import dataclass
from tkinter import ttk

from components.tree_panel import create_tree_panel


@dataclass
class MetadataPanel:
    """Metadata panel component."""

    frame: ttk.LabelFrame
    tree: ttk.Treeview

    @classmethod
    def create(cls, parent: tk.Widget) -> "MetadataPanel":
        """Create and place the metadata panel widgets."""
        frame, tree = create_tree_panel(parent, "Table metadata")

        tree["columns"] = ("column", "type")
        tree.heading("column", text="column")
        tree.heading("type", text="type")
        tree.column("column", width=200, anchor=tk.W)
        tree.column("type", width=120, anchor=tk.W)

        return cls(frame=frame, tree=tree)

    def clear(self) -> None:
        """Clear all rows from the metadata tree."""
        self.tree.delete(*self.tree.get_children())

    def update(self, metadata: list[tuple[str, str]]) -> None:
        """Render column metadata rows in the tree."""
        self.clear()
        for row in metadata:
            self.tree.insert("", tk.END, values=row)
