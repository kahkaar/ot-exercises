import tkinter as tk
from dataclasses import dataclass
from tkinter import ttk
from typing import Callable, Literal


@dataclass
class QueryPanel:
    """Panel for editing queries."""

    frame: ttk.LabelFrame
    query_text: tk.Text

    SHORTCUT_RUN_QUERY = "<F5>"

    @classmethod
    def create(
            cls,
            parent: tk.Widget,
            on_run_select: Callable[[], None],
            on_show_history: Callable[[], None]
    ) -> "QueryPanel":
        """Create query editor widgets."""
        frame = ttk.LabelFrame(parent, text="Query", padding=8)
        frame.grid(column=0, row=0, sticky=tk.NSEW)
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)
        query_text = tk.Text(frame, height=2, wrap="none")
        query_text.grid(column=0, row=0, sticky=tk.NSEW)
        button_frame = ttk.Frame(frame)
        button_frame.grid(column=0, row=1, sticky=tk.E, pady=(8, 0))
        ttk.Button(button_frame, text="Run SELECT",
                   command=on_run_select).pack(side=tk.LEFT, padx=(0, 8))
        if on_show_history is not None:
            ttk.Button(button_frame, text="Show History",
                       command=on_show_history).pack(side=tk.LEFT)

        def _on_shortcut(_=None) -> Literal["break"]:
            on_run_select()
            return "break"

        query_text.bind(cls.SHORTCUT_RUN_QUERY, _on_shortcut)
        return cls(frame=frame, query_text=query_text)

    def query(self) -> str:
        """Get query text from editor."""
        return self.query_text.get("1.0", tk.END).strip()
