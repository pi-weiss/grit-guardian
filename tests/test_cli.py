import pytest

from grit_guardian.cli import main


class TestCLIAdd:
    """Tests the 'add' command."""

    def test_add_habit_success(self, isolated_cli_runner):
        """Tests successfully adding a habit."""
        result = isolated_cli_runner.invoke(
            main, ["add", "Exercise", "Do 20 pushups", "daily"]
        )

        assert result.exit_code == 0  # command completed successfully
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
        """Tests adding habit with invalid periodicity."""
        result = isolated_cli_runner.invoke(
            main, ["add", "Exercise", "Do 20 pushups", "monthly"]
        )

        # Click should catch invalid choice
        assert result.exit_code != 0  # Command completed successfully
        assert "Invalid value for" in result.output

    def test_add_habit_weekly(self, isolated_cli_runner):
        """Tests adding weekly habit."""
        result = isolated_cli_runner.invoke(
            main, ["add", "Weekly Review", "Plan the week", "weekly"]
        )

        assert result.exit_code == 0
        assert "✓ Added habit 'Weekly Review' (weekly)" in result.output


class TestCLIList:
    """Tests the 'list' command."""

    def test_list_empty(self, isolated_cli_runner):
        """Tests listing when no habits exist."""
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
        list_result = isolated_cli_runner.invoke(main, ["list"])
        assert "Exercise" in list_result.output

    def test_delete_nonexistent_habit(self, isolated_cli_runner):
        """Tests deleting non-existent habit."""
        result = isolated_cli_runner.invoke(
            main, ["delete", "Nonexistent"], input="y\n"
        )

        assert result.exit_code == 0
        assert "✗" in result.output
        assert "not found" in result.output


class TestCLIComplete:
    """Tests the 'complete' command."""

    def test_complete_habit_success(self, isolated_cli_runner):
        """Tests successfully completing a habit."""
        # Add habit first
        isolated_cli_runner.invoke(main, ["add", "Exercise", "Do 20 pushups", "daily"])

        # Complete it
        result = isolated_cli_runner.invoke(main, ["complete", "Exercise"])

        assert result.exit_code == 0
        assert "✓ Completed 'Exercise'!" in result.output

    def test_complete_nonexistent_habit(self, isolated_cli_runner):
        """Tests completing non-existent habit."""
        result = isolated_cli_runner.invoke(main, ["complete", "Nonexistent"])

        assert result.exit_code == 0
        assert "✗" in result.output
        assert "not found" in result.output

    def test_complete_habit_already_done(self, isolated_cli_runner):
        """Tests completing habit that's already done today."""
        # Add and complete habit
        isolated_cli_runner.invoke(main, ["add", "Exercise", "Do 20 pushups", "daily"])
        isolated_cli_runner.invoke(main, ["complete", "Exercise"])

        # Try to complete again
        result = isolated_cli_runner.invoke(main, ["complete", "Exercise"])

        assert result.exit_code == 0
        assert "✗" in result.output
        assert "already been completed" in result.output


class TestCLIStatus:
    """Tests the 'status' command."""

    def test_status_no_habits(self, isolated_cli_runner):
        """Tests status when no habits exist."""
        result = isolated_cli_runner.invoke(main, ["status"])

        assert result.exit_code == 0
        assert "📊 Today's Status" in result.output
        assert "No habits found" in result.output

    def test_status_with_pending_habits(self, isolated_cli_runner):
        """Tests status with pending habits."""
        isolated_cli_runner.invoke(main, ["add", "Exercise", "Do 20 pushups", "daily"])
        isolated_cli_runner.invoke(main, ["add", "Reading", "Read 10 pages", "daily"])

        result = isolated_cli_runner.invoke(main, ["status"])

        assert result.exit_code == 0
        assert "⏳ Pending:" in result.output
        assert "Exercise" in result.output
        assert "Reading" in result.output
        assert "Progress: 0/2" in result.output

    def test_status_with_completed_habits(self, isolated_cli_runner):
        """Tests status with some completed habits."""
        isolated_cli_runner.invoke(main, ["add", "Exercise", "Do 20 pushups", "daily"])
        isolated_cli_runner.invoke(main, ["add", "Reading", "Read 10 pages", "daily"])
        isolated_cli_runner.invoke(main, ["complete", "Exercise"])

        result = isolated_cli_runner.invoke(main, ["status"])

        assert result.exit_code == 0
        assert "✅ Completed:" in result.output
        assert "⏳ Pending:" in result.output
        assert "Progress: 1/2" in result.output

    def test_status_all_completed(self, isolated_cli_runner):
        """Tests status when all habits are completed."""
        isolated_cli_runner.invoke(main, ["add", "Exercise", "Do 20 pushups", "daily"])
        isolated_cli_runner.invoke(main, ["complete", "Exercise"])

        result = isolated_cli_runner.invoke(main, ["status"])

        assert result.exit_code == 0
        assert "🎉 All habits completed!" in result.output
        assert "Progress: 1/1" in result.output


class TestCLIStreaks:
    """Tests the 'streaks' command."""

    def test_streaks_no_habits(self, isolated_cli_runner):
        """Tests streaks when no habits exist."""
        result = isolated_cli_runner.invoke(main, ["streaks"])

        assert result.exit_code == 0
        assert "No habits found" in result.output

    def test_streaks_with_habits(self, isolated_cli_runner):
        """Tests streaks display with habits."""
        isolated_cli_runner.invoke(main, ["add", "Exercise", "Do 20 pushups", "daily"])
        isolated_cli_runner.invoke(main, ["complete", "Exercise"])

        result = isolated_cli_runner.invoke(main, ["streaks"])

        assert result.exit_code == 0
        assert "🔥 Habit Streaks & Analytics" in result.output
        assert "📌 Exercise" in result.output
        assert "Current Streak:" in result.output
        assert "Longest Streak:" in result.output
        assert "Completion Rate:" in result.output
        assert "📊 Overall Stats:" in result.output


class TestCLIWeekly:
    """Tests the 'weekly' command."""

    def test_weekly_no_habits(self, isolated_cli_runner):
        """Tests weekly view with no habits."""
        result = isolated_cli_runner.invoke(main, ["weekly"])

        assert result.exit_code == 0
        assert "No habits to display" in result.output

    def test_weekly_with_habits(self, isolated_cli_runner):
        """Tests weekly view with habits."""
        isolated_cli_runner.invoke(main, ["add", "Exercise", "Do 20 pushups", "daily"])

        result = isolated_cli_runner.invoke(main, ["weekly"])

        assert result.exit_code == 0
        assert "📅 Weekly Progress" in result.output
        assert "Exercise" in result.output
        assert "Mon | Tue | Wed | Thu | Fri | Sat | Sun" in result.output
        assert "✓ = Completed  |  ✗ = Missed  |  - = Future" in result.output


class TestCLIStruggled:
    """Tests the 'struggled' command."""

    def test_struggled_no_habits(self, isolated_cli_runner):
        """Tests struggled habits when none exist."""
        result = isolated_cli_runner.invoke(main, ["struggled"])

        assert result.exit_code == 0
        assert "🌟 Great job! No struggled habits" in result.output

    def test_struggled_with_good_habits(self, isolated_cli_runner):
        """Tests struggled habits when all habits are doing well."""
        isolated_cli_runner.invoke(main, ["add", "Exercise", "Do 20 pushups", "daily"])
        isolated_cli_runner.invoke(main, ["complete", "Exercise"])

        result = isolated_cli_runner.invoke(main, ["struggled"])

        assert result.exit_code == 0
        assert "🌟 Great job! No struggled habits" in result.output

    def test_struggled_custom_days(self, isolated_cli_runner):
        """Tests struggled habits with custom day parameter."""
        result = isolated_cli_runner.invoke(main, ["struggled", "--since", "14"])

        assert result.exit_code == 0
        assert "last 14 days" in result.output
