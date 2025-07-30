import pytest

from grit_guardian.cli import main


# CliRunner provided by click.testing module
# See: https://click.palletsprojects.com/en/stable/testing/
@pytest.fixture
def cli_runner():
    """Creates Click testing runner.

    Returns:
        Click CliRunner instance
    """
    from click.testing import CliRunner

    return CliRunner()


# Use monkeypatch for database isolation
# Patch _get_default_db_path method with mock path
# Built on top of Click's CliRunner
# See: https://docs.pytest.org/en/stable/how-to/monkeypatch.html
@pytest.fixture
def isolated_cli_runner(monkeypatch, temp_db):
    """Creates isolated Click testing runner with test database.

    Args:
        monkeypatch: Pytest monkeypatch fixture
        temp_db: Temporary database path fixture

    Returns:
        Click CliRunner instance with isolated environment
    """
    from click.testing import CliRunner

    # Mock database path for CLI
    monkeypatch.setattr(
        "grit_guardian.persistence.database_manager.DatabaseManager._get_default_db_path",
        lambda self: temp_db,
    )

    return CliRunner()


class TestCLIAdd:
    """Tests the 'add' command."""

    def test_add_habit_success(self, isolated_cli_runner):
        """Tests successfully adding a habit."""
        result = isolated_cli_runner.invoke(
            main, ["add", "Exercise", "Do 20 pushups", "daily"]
        )

        assert result.exit_code == 0
        assert "✓ Added habit 'Exercise' (daily)" in result.output

    def test_add_habit_duplicate(self, isolated_cli_runner):
        """Tests adding duplicate habit shows error."""
        # Add first habit
        isolated_cli_runner.invoke(main, ["add", "Exercise", "Do 20 pushups", "daily"])

        # Try to add duplicate
        result = isolated_cli_runner.invoke(
            main, ["add", "Exercise", "Do 30 pushups", "daily"]
        )

        assert result.exit_code == 0
        assert "✗ Error:" in result.output
        assert "already exists" in result.output

    def test_add_habit_invalid_periodicity(self, isolated_cli_runner):
        """Test adding habit with invalid periodicity."""
        result = isolated_cli_runner.invoke(
            main, ["add", "Exercise", "Do 20 pushups", "monthly"]
        )

        # Click should catch invalid choice
        assert result.exit_code != 0
        assert "Invalid value for" in result.output

    def test_add_habit_weekly(self, isolated_cli_runner):
        """Test adding weekly habit."""
        result = isolated_cli_runner.invoke(
            main, ["add", "Weekly Review", "Plan the week", "weekly"]
        )

        assert result.exit_code == 0
        assert "✓ Added habit 'Weekly Review' (weekly)" in result.output


class TestCLIList:
    """Tests the 'list' command."""

    def test_list_empty(self, isolated_cli_runner):
        """Test listing when no habits exist."""
        result = isolated_cli_runner.invoke(main, ["list"])

        assert result.exit_code == 0
        assert "No habits found" in result.output
        assert "Add one with 'grit-guardian add'" in result.output

    def test_list_with_habits(self, isolated_cli_runner):
        """Tests listing existing habits."""
        # Add some habits first
        isolated_cli_runner.invoke(main, ["add", "Exercise", "Do 20 pushups", "daily"])
        isolated_cli_runner.invoke(main, ["add", "Reading", "Read 10 pages", "weekly"])

        result = isolated_cli_runner.invoke(main, ["list"])

        assert result.exit_code == 0
        assert "Your Habits:" in result.output
        assert "Exercise - Do 20 pushups (daily)" in result.output
        assert "Reading - Read 10 pages (weekly)" in result.output


class TestCLIDelete:
    """Tests the 'delete' command."""

    def test_delete_habit_confirmed(self, isolated_cli_runner):
        """Tests deleting habit with confirmation."""
        # Add habit first
        isolated_cli_runner.invoke(main, ["add", "Exercise", "Do 20 pushups", "daily"])

        # Delete with confirmation
        result = isolated_cli_runner.invoke(main, ["delete", "Exercise"], input="y\n")

        assert result.exit_code == 0
        assert "✓ Deleted habit 'Exercise'" in result.output

    def test_delete_habit_cancelled(self, isolated_cli_runner):
        """Tests cancelling habit deletion."""
        # Add habit first
        isolated_cli_runner.invoke(main, ["add", "Exercise", "Do 20 pushups", "daily"])

        # Cancel deletion
        result = isolated_cli_runner.invoke(main, ["delete", "Exercise"], input="n\n")

        assert result.exit_code == 0
        assert "Aborted" in result.output

    def test_delete_nonexistent_habit(self, isolated_cli_runner):
        """Tests deleting non-existent habit."""
        result = isolated_cli_runner.invoke(
            main, ["delete", "Nonexistent"], input="y\n"
        )

        assert result.exit_code == 0
        assert "✗" in result.output
        assert "not found" in result.output
