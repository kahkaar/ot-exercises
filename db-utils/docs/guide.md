# User Guide

This guide explains how to use the db-utils application for browsing and exporting data from local SQLite databases.

## Starting the Application

1. Open a terminal and navigate to the project directory (where main.py is located).
2. Run the application with:

   ```bash
   poetry run invoke start
   ```

The main window will open.

## Opening a Database

- Click the button or menu to select a database file.
- Browse to the desired SQLite database file and confirm your selection.
- The list of tables in the database will appear on the left.

## Viewing Table Metadata

- Click on any table in the list to see its columns and types in the metadata panel.

## Running Queries

- Use the query editor to write a SELECT statement.
- Press the "Run SELECT" button or use the F5 shortcut to execute the query.
- The results will be shown in the results panel.

## Exporting Results

- After running a query, you can export the results:
  - Click "Export CSV" to save as a CSV file.
  - Click "Export JSON" to save as a JSON file.
- Choose the location and filename when prompted.

## Query History

- The application saves your previous queries.
- You can view and reuse past queries from the query panel.

## Status and Error Messages

- Status updates and error messages are shown in the status area.

## Exiting the Application

- Close the window or use the standard quit command for your operating system.

---

For more details, see the architecture documentation or source code.
