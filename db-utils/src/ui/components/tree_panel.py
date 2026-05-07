import tkinter as tk
from tkinter import ttk
from typing import Tuple


def create_tree_panel(parent: tk.Widget, title: str) -> Tuple[ttk.LabelFrame, ttk.Treeview]:
    """Create a labeled tree panel."""

    frame = ttk.LabelFrame(parent, text=title, padding=8)
    frame.grid(column=0, row=1, sticky=tk.NSEW, pady=(12, 0))
    frame.columnconfigure(0, weight=1)
    frame.rowconfigure(0, weight=1)

    container = ttk.Frame(frame)
    container.grid(column=0, row=0, sticky=tk.NSEW)
    container.columnconfigure(0, weight=1)
    container.rowconfigure(0, weight=1)

    tree = ttk.Treeview(container, show="headings")
    scroll_y = ttk.Scrollbar(container, orient=tk.VERTICAL, command=tree.yview)
    scroll_x = ttk.Scrollbar(
        container, orient=tk.HORIZONTAL, command=tree.xview)
    tree.configure(
        yscrollcommand=scroll_y.set,
        xscrollcommand=scroll_x.set,
    )

    tree.grid(column=0, row=0, sticky=tk.NSEW)
    scroll_y.grid(column=1, row=0, sticky=tk.NS)
    scroll_x.grid(column=0, row=1, sticky=tk.EW)

    return frame, tree
