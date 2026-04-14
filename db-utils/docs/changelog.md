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
