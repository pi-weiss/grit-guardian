import pytest
import sqlite3
import tempfile
from pathlib import Path
from datetime import datetime, timedelta
from grit_guardian.persistence.database_manager import DatabaseManager


class TestDatabaseManager:
    def test_database_creation(self, temp_db):
        """Tests that database and tables are created correctly."""
        assert temp_db.db_path.exists()

        with sqlite3.connect(temp_db.db_path) as conn:
            tables = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table';"
            ).fetchall()
            table_names = [t[0] for t in tables]

            assert "habits" in table_names
            assert "completions" in table_names

    # https://docs.pytest.org/en/stable/how-to/skipping.html#skip
    # @pytest.mark.skip(reason="Full DB logic not yet implemented.")
    def test_create_habit_success(self, temp_db):
        """Tests creating a habit successfully."""
        habit_id = temp_db.create_habit(
            name="Wolf", task="Howl 10 minutes at the moon", periodicity="daily"
        )

        assert isinstance(habit_id, int)
        assert habit_id > 0

        # Verify habit was created
        habit = temp_db.get_habit_by_name("Wolf")
        assert habit is not None
        assert habit["name"] == "Wolf"
        assert habit["task"] == "Howl 10 minutes at the moon"
        assert habit["periodicity"] == "daily"

    # @pytest.mark.skip(reason="Full DB logic not yet implemented.")
    def test_create_habit_duplicate_name(self, temp_db):
        """Tests that creating a habit with duplicate name fails."""
        temp_db.create_habit("Exercise", "Run", "daily")

        with pytest.raises(sqlite3.IntegrityError):
            temp_db.create_habit("Exercise", "Different task", "weekly")

    # @pytest.mark.skip(reason="Full DB logic not yet implemented.")
    def test_create_habit_invalid_periodicity(self, temp_db):
        """Tests that invalid periodicity raises ValueError."""
        with pytest.raises(ValueError, match="Invalid periodicity"):
            temp_db.create_habit(
                "Exercise", "Run", "yearly"
            )  # Will not accept lazyness

    # @pytest.mark.skip(reason="Full DB logic not yet implemented.")
    def test_get_habits_empty(self, temp_db):
        """Tests getting habits when none exist."""
        habits = temp_db.get_habits()
        assert habits == []

    # @pytest.mark.skip(reason="Full DB logic not yet implemented.")
    def test_get_habits_with_data(self, temp_db):
        """Tests getting all habits with completion counts."""
        # Create habit
        habit1_id = temp_db.create_habit(
            "Crazy", "Laugh hysterically for 10 seconds for no reason", "daily"
        )
        habit2_id = temp_db.create_habit("Read", "Read 20 pages", "daily")

        assert habit1_id > 0
        assert habit2_id > 0

        # Add completions
        temp_db.add_completion("Crazy")
        temp_db.add_completion("Crazy")
        temp_db.add_completion("Read")

        habits = temp_db.get_habits()
        assert len(habits) == 2

        # Find habits by name
        crazy = next(h for h in habits if h["name"] == "Crazy")
        read = next(h for h in habits if h["name"] == "Read")

        assert crazy["total_completions"] == 2
        assert read["total_completions"] == 1
        assert crazy["last_completed"] is not None
        assert read["last_completed"] is not None

    # @pytest.mark.skip(reason="Full DB logic not yet implemented.")
    def test_get_habit_by_name(self, temp_db):
        """Tests getting a specific habit by name"""
        temp_db.create_habit("Exercise", "Run", "daily")

        habit = temp_db.get_habit_by_name("Exercise")
        assert habit is not None
        assert habit["name"] == "Exercise"

        # Non-existent habit
        habit = temp_db.get_habit_by_name("NonExistent")
        assert habit is None

    # @pytest.mark.skip(reason="Full DB logic not yet implemented.")
    def test_delete_habit(self, temp_db):
        """Tests deleteing a habit."""
        temp_db.create_habit("Exercise", "Run", "daily")
        temp_db.add_completion("Exercise")

        # Delete the habit
        deleted = temp_db.delete_habit("Exercise")
        assert deleted is True

        # Verify completions are also gone (cascade delete)
        completions = temp_db.get_completions("Exercise")
        assert completions == []

        # Try deleting Non-existent habit
        deleted = temp_db.delete_habit("NonExistent")
        assert deleted is False

    # @pytest.mark.skip(reason="Full DB logic not yet implemented.")
    def test_add_completion(self, temp_db):
        """Tests adding a completion to a habit."""
        temp_db.create_habit("Exercise", "Run", "daily")

        completion_id = temp_db.add_completion("Exercise")
        assert isinstance(completion_id, int)
        assert completion_id > 0

        # Verify completion was added
        completions = temp_db.get_completions("Exercise")
        assert len(completions) == 1
        assert isinstance(completions[0], datetime)

    # @pytest.mark.skip(reason="Full DB logic not yet implemented.")
    def test_add_completion_with_custom_date(self, temp_db):
        """Tests adding a completion with custom timestamp."""
        temp_db.create_habit("Exercise", "Run", "daily")

        custom_date = datetime.now() - timedelta(days=2)
        temp_db.add_completion("Exercise", custom_date)

        completions = temp_db.get_completions("Exercise")
        assert len(completions) == 1

        # Test with custom date in the future
        future_date = datetime.now() + timedelta(days=1)

        with pytest.raises(ValueError, match="Completion date cannot be in the future"):
            temp_db.add_completion("Exercise", future_date)

        # Compare timestamps without microseconds
        assert completions[0].replace(microsecond=0) == custom_date.replace(
            microsecond=0
        )

    # @pytest.mark.skip(reason="Full DB logic not yet implemented.")
    def test_add_completion_nonexistent_habit(self, temp_db):
        """Tests that adding completion to non-existent habit fails."""
        with pytest.raises(ValueError, match="Habit 'NonExistent' not found"):
            temp_db.add_completion("NonExistent")

    # @pytest.mark.skip(reason="Full DB logic not yet implemented.")
    def test_get_completions(self, temp_db):
        """Tests getting completions for a habit."""
        temp_db.create_habit("Exercise", "Run", "daily")

        # Add multiple completions
        now = datetime.now()
        for i in range(3):
            temp_db.add_completion(
                "Exercise", now - timedelta(days=i)
            )  # Courtesy of 'The Farmer Was Replaced'

        # Get all completions
        completions = temp_db.get_completions("Exercise")
        assert len(completions) == 3

        # Should be ordered by most recent first
        assert completions[0] > completions[1] > completions[2]

        # Test with limit
        limited = temp_db.get_completions("Exercise", limit=2)
        assert len(limited) == 2
        assert limited == completions[:2]

    # @pytest.mark.skip(reason="Full DB logic not yet implemented.")
    def test_foreign_key_constraint(self, temp_db):
        """Tests that foreign key constraints are enforced."""
        with temp_db._get_connection() as conn:
            # Try to insert completion for non-existent habit
            with pytest.raises(sqlite3.IntegrityError):
                conn.execute(
                    "INSERT INTO completions (habit_id, completed_at) VALUES (?, ?);",
                    (9999, datetime.now()),
                )

    # @pytest.mark.skip(reason="Full DB logic not yet implemented.")
    def test_backup_database(self, temp_db):
        """Tests database backup functionality."""
        # Add some data
        temp_db.create_habit(
            "Scarecrow", "Stand in the middle of a field for 1 hour", "weekly"
        )
        temp_db.add_completion("Scarecrow")

        # Create backup
        backup_path = temp_db.backup_database()
        assert backup_path.exists()

        # Verify backup contains data
        backup_db = DatabaseManager(backup_path)
        habits = backup_db.get_habits()
        assert len(habits) == 1
        assert habits[0]["name"] == "Scarecrow"

    # @pytest.mark.skip(reason="Full DB logic not yet implemented.")
    def test_get_stats(self, temp_db):
        """Tests getting database statistics."""
        # Empty stats
        stats = temp_db.get_stats()
        assert stats["total_habits"] == 0
        assert stats["total_completions"] == 0
        assert stats["habits_by_periodicity"] == {}

        # Add data
        temp_db.create_habit("Exercise", "Run", "daily")
        temp_db.create_habit("Read", "Read 20 pages", "daily")
        temp_db.create_habit("Review", "Weekly review", "weekly")

        temp_db.add_completion("Exercise")
        temp_db.add_completion("Read")
        temp_db.add_completion("Review")

        # Get stats
        stats = temp_db.get_stats()
        assert stats["total_habits"] == 3
        assert stats["total_completions"] == 3
        assert stats["habits_by_periodicity"]["daily"] == 2
        assert stats["habits_by_periodicity"]["weekly"] == 1

    # @pytest.mark.skip(reason="Full DB logic not yet implemented.")
    def test_default_path(self):
        """Tests that default paht follows XDG specification."""
        db = DatabaseManager()
        expected_path = Path.home() / ".config" / "grit-guardian" / "habits.db"
        assert db.db_path == expected_path

        # Clean up (don't actually create the file)
        if db.db_path.exists():
            db.db_path.unlink()


# @pytest.mark.skip(reason="Full DB logic not yet implemented.")
class TestDatabaseCorruption:
    def test_restore_from_backup(self, temp_db):
        """Tests database restoration from backup."""
        # Add data and create backup
        temp_db.create_habit("Exercise", "Run", "daily")
        backup_path = temp_db.backup_database()

        assert backup_path.exists()

        # Corrupt the database
        with open(temp_db.db_path, "wb") as f:
            f.write(b"corrupted data")

        # Try an operation that should trigger restoration
        with pytest.raises(Exception, match="Database was corrupted"):
            temp_db.get_habits()

        # Verify database was restored
        habits = temp_db.get_habits()
        assert len(habits) == 1
        assert habits[0]["name"] == "Exercise"

    def test_restore_without_backup(self, temp_db):
        """Tests handling corruption when no backup exists."""
        # Corrupt the database without creating backup
        with open(temp_db.db_path, "wb") as f:
            f.write(b"corrupted data")

        # Try an operation
        with pytest.raises(Exception, match="Database was corrupted"):
            temp_db.get_habits()

        # Verify corrupted file was moved aside
        corrupted_path = temp_db.db_path.with_suffix(".db.corrupted")
        assert corrupted_path.exists()

        # Verify new database was created
        habits = temp_db.get_habits()
        assert habits == []
