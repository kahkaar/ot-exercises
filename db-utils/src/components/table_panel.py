import tkinter as tk
from dataclasses import dataclass
from tkinter import ttk
from typing import Callable


@dataclass
class TablePanel:
    """Table list panel component."""

    frame: ttk.LabelFrame
    table_listbox: tk.Listbox

    @classmethod
    def create(
        cls,
        parent: tk.Widget,
        on_select: Callable[[], None],
    ) -> "TablePanel":
        """Create and place the table panel widgets."""
        frame = ttk.LabelFrame(parent, text="Tables", padding=8)
        frame.grid(column=0, row=0, sticky=tk.NSEW)

        table_listbox = tk.Listbox(frame, height=10, width=40)
        table_listbox.pack(fill=tk.BOTH, expand=True)
        table_listbox.bind("<<ListboxSelect>>", lambda _event: on_select())

        table_button_frame = ttk.Frame(frame)
        table_button_frame.pack(fill=tk.X, pady=(8, 0))

        return cls(frame=frame, table_listbox=table_listbox)

    def update_tables(self, tables: list[str]) -> None:
        """Replace table list items with a new set of names."""
        self.table_listbox.delete(0, tk.END)
        for table in tables:
            self.table_listbox.insert(tk.END, table)

    def selected_table_name(self) -> str | None:
        """Return the currently selected table name, if any."""
        selection = self.table_listbox.curselection()
        if not selection:
            return None
        return str(self.table_listbox.get(int(selection[0])))
