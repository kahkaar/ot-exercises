# Architecture

## High-Level Structure

The project is organized into a few clear parts:

- `main.py`: Starts the program. Sets up the main window and launches the UI.
- `ui/`: Contains the user interface components.
  - `gui.py`: Manages the main window and overall workflow. This is where the UI panels and services are created and connected.
  - `components/`: All the main UI panels live here:
    - `TablePanel`: Shows the list of tables in the database.
    - `MetadataPanel`: Displays column info for the selected table and whole database schema.
    - `QueryPanel`: Lets the user write and run SELECT queries.
    - `ResultsPanel`: Shows query results and lets you export them.
    - `TreePanel`: Shared helper for tree-style views.
- `services/`: Handles the actual logic and database work:
  - `DatabaseService`: Checks the SQLite database, lists tables, fetches metadata, and runs queries.
  - `ExportService`: Exports data to CSV and JSON files.
  - `QueryHistoryService`: Saves and loads previous queries for convenience.

## Application Logic

1. Startup: The program begins in main.py, which creates the Tkinter window and the UI object.
2. UI: The UI sets up all the panels: tables, metadata, query editor, and results.
3. Open Database: The user picks a database file. The UI asks DatabaseService to check the file and list the tables.
4. Select Table: When a table is selected, the UI fetches its metadata and updates the MetadataPanel.
5. Run Query: The user writes a SELECT query and runs it. The UI gets the results from DatabaseService and updates the ResultsPanel.
6. Export Results: Results can be exported to CSV or JSON. The ResultsPanel uses ExportService for this.

## Class Diagram

```mermaid
classDiagram

class Main {
  application entry
}

class UI {
  main window and workflow controller
}

class DatabaseService {
  SQLite database access
}

class ExportService {
  export logic
}

class TablePanel {
  table list
}

class MetadataPanel {
  table metadata
}

class QueryPanel {
  query editor
}

class ResultsPanel {
  query results
}

class QueryHistoryService {
  query saving/loading
}

class UIComponents {
  panel references
}

Main ..> UI
UI *-- UIComponents
UI --> DatabaseService
UI --> QueryHistoryService
UIComponents o-- TablePanel
UIComponents o-- MetadataPanel
UIComponents o-- QueryPanel
UIComponents o-- ResultsPanel
ResultsPanel --> ExportService
QueryPanel --> QueryHistoryService
```

## Application Sequence

```mermaid
sequenceDiagram
  participant Main as main.py
  participant UI as UI (gui.py)
  participant TablePanel as TablePanel
  participant MetadataPanel as MetadataPanel
  participant QueryPanel as QueryPanel
  participant ResultsPanel as ResultsPanel
  participant DatabaseService as DatabaseService
  participant ExportService as ExportService

  Main->>UI: create UI(root)
  UI->>TablePanel: create (table list)
  UI->>MetadataPanel: create (table metadata)
  UI->>QueryPanel: create (query editor)
  UI->>ResultsPanel: create (query results)

  Note over UI: User clicks "Open..."
  UI->>DatabaseService: validate(path)
  DatabaseService-->>UI: validation result
  UI->>DatabaseService: list_tables()
  DatabaseService-->>UI: table names
  UI->>TablePanel: update_tables(tables)

  Note over UI: User selects table
  UI->>DatabaseService: get_table_metadata(table)
  DatabaseService-->>UI: metadata

  UI->>MetadataPanel: update(metadata)
  Note over UI: User runs SELECT query

  UI->>DatabaseService: run_select_query(query)
  DatabaseService-->>UI: columns, rows
  UI->>ResultsPanel: update(columns, rows)

  Note over UI: User exports results
  ResultsPanel->>ExportService: to_csv/to_json(columns, rows, path)
```
