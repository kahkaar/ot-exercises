import tkinter as tk

from ui.gui import UI


def main() -> None:
    """Main entry point for the db-utils application."""

    window = tk.Tk()
    window.title("db-utils")
    window.geometry("1200x900")

    ui = UI(root=window)
    ui.start()


if __name__ == "__main__":
    main()
