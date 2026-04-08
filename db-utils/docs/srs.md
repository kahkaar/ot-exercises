# db-utils

This document describes what db-utils should do and what constraints affect its implementation.

## Software Requirements Specification

db-utils is a Python desktop application built with tkinter for inspecting local SQLite databases and exporting data.

### Features

The local user should be able to:

- [x] open a local SQLite database file through the GUI
- [x] view the list of tables in the selected database
- [x] run SELECT queries from the GUI
- [x] view query results inside the application
- [ ] export table data or query results to `csv`
- [ ] export table data or query results to `json`
- [ ] inspect basic table metadata (for example, column names and types)
- [ ] receive clear error messages for invalid paths, malformed SQL, and file write failures

### Further Development Ideas

- [ ] view the full database schema
- [ ] start the application from the CLI with a database path, for example: `db-utils /path/to/file.db`
- [ ] support additional export formats
- [ ] additional improvements identified during development

### Environment and Constraints

- The application is implemented in Python.
- The GUI toolkit is tkinter.
- The supported database engine is SQLite.
- SQL support is limited to SQLite-compatible syntax.
- The application works with local files only.
- The application should run on Linux (**Ubuntu 24.04** and **Cubbli 24**).
- Typical operations with normal local datasets should feel responsive.
- Exported files must be valid UTF-8 `csv` or `json`.

### Testing

The project should include automated and manual testing.

- Unit tests should cover core logic such as query handling, validation, and export formatting.
- Integration tests should verify behavior with a sample SQLite database file.
- Export tests should verify that generated `csv` and `json` files are readable and correctly encoded in UTF-8.
- Manual tests should confirm that key GUI flows work: opening a database, running a SELECT query, viewing results, and exporting data.

### Out of Scope

The following are intentionally excluded from this version:

- authentication, authorization, and multi-user features
- editing database rows (INSERT, UPDATE, DELETE)
- remote database connections

### User Interface

The GUI should include:

- a database file selector
- a table list panel
- a query editor area
- a results table view
- export actions for `csv` and `json`
- a visible area for status and error messages
