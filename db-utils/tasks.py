from invoke.context import Context
from invoke.tasks import task


@task
def start(ctx: Context) -> None:
    """Start the database utility GUI."""
    ctx.run("python3 src/main.py")


@task
def lint(ctx: Context) -> None:
    """Run linting on the source code."""
    ctx.run("pylint src/")


@task(pre=[lint])
def test(ctx: Context) -> None:
    """Run tests on the source code."""
    ctx.run("pytest tests/")


@task
def coverage(ctx: Context) -> None:
    """Run tests with coverage measurement."""
    ctx.run("coverage run --branch -m pytest tests/")


@task(pre=[coverage])
def coverage_report(ctx: Context) -> None:
    """Generate a coverage report and open it in the default web browser."""
    ctx.run("coverage html")
