# Changelog

## Week 3

### Added

- `UI` class in [`gui.py`](/db-utils/src/gui.py) with Tkinter
- `DatabaseService` class in [`services/database.py`](/db-utils/src/services/database.py) to handle database validation and table listing
- Ability to open a local SQLite database file through the GUI
- Ability to view all tables in the local SQLite database
- Created `invoke` tasks in [`tasks.py`](/db-utils/tasks.py)
- Unit tests for the `DatabaseService` class.

## Week 4

### Added

- Ability to run `SELECT` queries and view results in the GUI
- Ability to inspect table metadata (column names and types)
- Added unit tests for metadata handling and edge cases in [`test_database_service.py`](/db-utils/tests/test_database_service.py)
- Added architecture docs

### Changed

- Refactored [`gui.py`](/db-utils/src/gui.py) to use UI components under [`src/components/`](/db-utils/src/components/)

## Week 5

### Added

- Ability to export query results to CSV and JSON formats through the GUI
- User can press F5 to run the current query in the query panel
- Added a sequence diagram to the architecture docs

### Changed

- Updated docstrings to be consistent and compact for all public methods in the codebase
- Updated typing annotations to be more precise and consistent across the codebase
- Updated architecture docs to include `ExportService` and its relationship with `ResultsPanel`
