import tkinter as tk
from dataclasses import dataclass
from tkinter import ttk
from typing import Callable


@dataclass
class QueryPanel:
    """Query editor panel component."""

    frame: ttk.LabelFrame
    query_text: tk.Text

    @classmethod
    def create(cls, parent: tk.Widget, on_run_select: Callable[[], None]) -> "QueryPanel":
        """Create and place the query editor widgets."""
        frame = ttk.LabelFrame(parent, text="Query", padding=8)
        frame.grid(column=0, row=0, sticky=tk.NSEW)
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)

        query_text = tk.Text(frame, height=2, wrap="none")
        query_text.grid(column=0, row=0, sticky=tk.NSEW)

        button_frame = ttk.Frame(frame)
        button_frame.grid(column=0, row=1, sticky=tk.E, pady=(8, 0))
        ttk.Button(button_frame, text="Run SELECT",
                   command=on_run_select).pack()

        return cls(frame=frame, query_text=query_text)

    def query(self) -> str:
        """Return the normalized query text from the editor."""
        return self.query_text.get("1.0", tk.END).strip()
