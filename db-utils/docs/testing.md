# Test Report

Unit tests for the service modules live in [`tests/`](/db-utils/tests/).

## Test Modules

- [`tests/test_database_service.py`](/db-utils/tests/test_database_service.py): DatabaseService: validation, table listing, select queries, metadata, full schema.
- [`tests/test_export_service.py`](/db-utils/tests/test_export_service.py): ExportService: CSV/JSON output and error handling.
- [`tests/test_query_history_service.py`](/db-utils/tests/test_query_history_service.py): QueryHistoryService: save/load, duplicates, empty queries, ordering.

## Running Tests

- To run all tests:

  ```bash
  poetry run invoke test
  ```

- To run tests with coverage:

  ```bash
  poetry run invoke coverage
  ```

- To run and view the coverage report:
  ```bash
  poetry run invoke coverage-report
  ```

## Coverage Report

The tests cover 95% of the _business logic_ branching in `db_utils/services/`.

![Coverage Report](/db-utils/docs/images/coverage.png)

The UI components are not covered by these tests.
