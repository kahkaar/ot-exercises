## ot-exercises

This repository contains the project source code and the weekly exercises for the _Intermediate Studies Project: Software Development Methods_ [`TKT20018`](https://studies.helsinki.fi/courses/course-unit/otm-fc35db8b-596c-4287-a03c-047e81e1254b/TKT20018?cpId=hy-lv-76) course at the **University of Helsinki**, as described in the [course material](https://ohjelmistotekniikka-hy.github.io/).

# Project: db-utils

A utility application for inspecting local SQLite databases and exporting table and query results as `.csv` and `.json` files.

The source code is located under the [`db-utils/`](/db-utils/) directory.
Documentation for the project is located in [`db-utils/docs/`](/db-utils/docs/).

## Installation

1. Install dependencies:

   ```bash
   poetry install
   ```

2. Start the application:
   ```bash
   poetry run invoke start
   ```

## Invoke Tasks

- List the available tasks:

  ```bash
  poetry run invoke --list
  ```

- Run lint:

  ```bash
  poetry run invoke lint
  ```

- Run tests:

  ```bash
  poetry run invoke test
  ```

> [!NOTE]
>
> The `test` task runs the `lint` task before executing tests.

- Run test coverage:

  ```bash
  poetry run invoke coverage
  ```

- Generate the HTML coverage report:
  ```bash
  poetry run invoke coverage-report
  ```

## Documentation

- [Changelog](./changelog.md)
- [Software Requirements Specification](./srs.md)
- [Time Logs](./time_logs.md)
