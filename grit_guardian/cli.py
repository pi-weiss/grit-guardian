import click

from grit_guardian.core.habit_tracker import HabitTracker
from grit_guardian.persistence.database_manager import DatabaseManager

db_manager = DatabaseManager()
tracker = HabitTracker(db_manager)


@click.group()
def main():
    """Grit Guardian - CLI habit tracker."""
    pass


@main.command()
@click.argument("name")
@click.argument("task")
@click.argument("periodicity", type=click.Choice(["daily", "weekly"]))
def add(name, task, periodicity):
    """Adds a new habit to track."""
    pass


@main.command()
def list():
    """Lists all habits."""
    pass


@main.command()
@click.argument("name")
def delete(name):
    """Deletes a habit."""
    pass


if __name__ == "__main__":
    main()
