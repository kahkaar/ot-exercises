import tkinter as tk
from dataclasses import dataclass
from tkinter import ttk
from typing import List, Tuple

from components.tree_panel import create_tree_panel


@dataclass
class MetadataPanel:
    """Panel for table metadata."""

    frame: ttk.LabelFrame
    tree: ttk.Treeview

    @classmethod
    def create(cls, parent: tk.Widget) -> "MetadataPanel":
        """Create metadata panel widgets."""
        frame, tree = create_tree_panel(parent, "Table metadata")
        tree["columns"] = ("column", "type")
        tree.heading("column", text="column")
        tree.heading("type", text="type")
        tree.column("column", width=200, anchor=tk.W)
        tree.column("type", width=120, anchor=tk.W)
        return cls(frame=frame, tree=tree)

    def clear(self) -> None:
        """Clear all rows from the tree."""
        self.tree.delete(*self.tree.get_children())

    def update(self, metadata: List[Tuple[str, str]]) -> None:
        """Update tree with column metadata."""
        self.clear()
        for row in metadata:
            self.tree.insert("", tk.END, values=row)
