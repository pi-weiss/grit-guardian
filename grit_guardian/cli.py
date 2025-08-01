import click

from grit_guardian.core.habit_tracker import HabitTracker
from grit_guardian.persistence.database_manager import DatabaseManager

_tracker = None


# Lazy loading the DatabaseManager instance to prevent initializing
# before test fixtures can patch the database path
def get_tracker():
    """Get or create the HabitTracker instance."""
    global _tracker
    if _tracker is None:
        db_manager = DatabaseManager()
        _tracker = HabitTracker(db_manager)
    return _tracker


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
    try:
        habit = get_tracker().add_habit(name, task, periodicity)
        click.echo(f"✓ Added habit '{habit.name}' ({habit.periodicity.value})")
    except Exception as e:
        click.echo(f"✗ Error: {str(e)}", err=True)


@main.command()
def list():
    """Lists all habits."""
    habits = get_tracker().list_habits()
    if not habits:
        click.echo("No habits found. Add one with 'grit-guardian add'")
        return

    click.echo("\nYour Habits:")
    click.echo("-" * 50)
    for habit in habits:
        click.echo(f"• {habit.name} - {habit.task} ({habit.periodicity.value})")


@main.command()
@click.argument("name")
def delete(name):
    """Deletes a habit."""
    if click.confirm(f"Delete habit '{name}'?"):
        try:
            get_tracker().delete_habit(name)
            click.echo(f"✓ Deleted habit '{name}'")
        except Exception as e:
            click.echo(f"✗ {str(e)}", err=True)


@main.command()
@click.argument("name")
def complete(name):
    """Marks a habit as completed"""
    try:
        get_tracker().complete_habit(name)
        click.echo(f"✓ Completed '{name}'!")
    except Exception as e:
        click.echo(f"✗ {str(e)}", err=True)


@main.command()
def status():
    """Show today's habit status"""
    status = get_tracker().get_status()

    click.echo("\n📊 Today's Status")
    click.echo("=" * 30)

    if status["pending"]:
        click.echo("\n⏳ Pending:")
        for habit in status["pending"]:
            click.echo(f"  • {habit.name}")

    if status["completed"]:
        click.echo("\n✅ Completed:")
        for habit in status["completed"]:
            click.echo(f"  • {habit.name}")

    if not status["pending"] and not status["completed"]:
        click.echo("\nNo habits found. Add one with 'grit-guardian add'")
    else:
        click.echo(f"\nProgress: {len(status['completed'])}/{status['total']}")
        if len(status["completed"]) == status["total"] and status["total"] > 0:
            click.echo("🎉 All habits completed!")


@main.command()
def streaks():
    """View current streaks and completion rates for all habits."""
    pass


if __name__ == "__main__":
    main()
