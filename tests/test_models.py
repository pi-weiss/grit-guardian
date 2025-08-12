import pytest
from datetime import datetime, timedelta

from grit_guardian.core import Habit, Periodicity


class TestPeriodicityEnum:
    """Tests the Periodicity enum."""

    def test_periodicity_values(self):
        """Tests that Periodicity enum has correct values."""
        assert Periodicity.DAILY.value == "daily"
        assert Periodicity.WEEKLY.value == "weekly"

    def test_periodicity_from_string(self):
        """Tests creating Periodicity from string value."""
        assert Periodicity("daily") == Periodicity.DAILY
        assert Periodicity("weekly") == Periodicity.WEEKLY

    def test_invalid_periodicity(self):
        """Tests that invalid periodicity raises ValueError."""
        with pytest.raises(ValueError):
            Periodicity("monthly")


class TestHabitModel:
    """Tests the Habit model class."""

    def test_habit_creation(self):
        """Tests creating a valid habit."""
        habit = Habit(
            id=1,
            name="Morning Exercise",
            task="Do 20 pushups",
            periodicity=Periodicity.DAILY,
            created_at=datetime.now(),
        )

        assert habit.id == 1
        assert habit.name == "Morning Exercise"
        assert habit.task == "Do 20 pushups"
        assert habit.periodicity == Periodicity.DAILY
        assert habit.completions == []

    def test_habit_creation_with_string_periodicity(self):
        """Tests that string periodicity is converted to enum."""
        habit = Habit(
            id=1,
            name="Test Habit",
            task="Test Task",
            periodicity="daily",  # String instead of enum
            created_at=datetime.now(),
        )

        assert habit.periodicity == Periodicity.DAILY

    def test_habit_validation_empty_name(self):
        """Test that empty name raises ValueError."""
        with pytest.raises(ValueError, match="Habit name cannot be empty"):
            Habit(
                id=1,
                name="",
                task="Test Task",
                periodicity=Periodicity.DAILY,
                created_at=datetime.now(),
            )

    def test_habit_validation_whitespace_name(self):
        """Tests that whitespace-only name raises ValueError."""
        with pytest.raises(ValueError, match="Habit name cannot be empty"):
            Habit(
                id=1,
                name="   ",
                task="Test Task",
                periodicity=Periodicity.DAILY,
                created_at=datetime.now(),
            )

    def test_habit_validation_empty_task(self):
        """Test that empty task raises ValueError."""
        with pytest.raises(ValueError, match="Habit task cannot be empty"):
            Habit(
                id=1,
                name="Test Habit",
                task="",
                periodicity=Periodicity.DAILY,
                created_at=datetime.now(),
            )

    def test_habit_validation_invalid_periodicity(self):
        """Test that invalid periodicity string raises ValueError."""
        with pytest.raises(ValueError, match="Invalid periodicity"):
            Habit(
                id=1,
                name="Test Habit",
                task="Test Task",
                periodicity="monthly",  # Invalid
                created_at=datetime.now(),
            )

    def test_habit_validation_future_date(self):
        """Test that future creation date raises ValueError."""
        future_date = datetime.now() + timedelta(days=1)
        with pytest.raises(ValueError, match="Creation date cannot be in the future"):
            Habit(
                id=1,
                name="Test Habit",
                task="Test Task",
                periodicity=Periodicity.DAILY,
                created_at=future_date,
            )

    def test_from_db_row(self):
        """Tests creating Habit from database row."""
        db_row = {
            "id": 1,
            "name": "Morning Exercise",
            "task": "Do 20 pushups",
            "periodicity": "daily",
            "created_at": datetime.now(),
        }

        habit = Habit.from_db_row(db_row)

        assert habit.id == 1
        assert habit.name == "Morning Exercise"
        assert habit.task == "Do 20 pushups"
        assert habit.periodicity == Periodicity.DAILY
        assert habit.completions == []

    def test_add_completion(self):
        """Tests adding a completion to a habit."""
        habit = Habit(
            id=1,
            name="Test Habit",
            task="Test Task",
            periodicity=Periodicity.DAILY,
            created_at=datetime.now(),
        )

        completion_date = datetime.now()
        habit.add_completion(completion_date)

        assert len(habit.completions) == 1
        assert habit.completions[0] == completion_date

    def test_add_completion_no_date(self):
        """Tests adding a completion without specifying date."""
        habit = Habit(
            id=1,
            name="Test Habit",
            task="Test Task",
            periodicity=Periodicity.DAILY,
            created_at=datetime.now(),
        )

        habit.add_completion()

        assert len(habit.completions) == 1
        assert isinstance(habit.completions[0], datetime)

    def test_add_completion_future_date(self):
        """Test that future completion date raises ValueError."""
        habit = Habit(
            id=1,
            name="Test Habit",
            task="Test Task",
            periodicity=Periodicity.DAILY,
            created_at=datetime.now(),
        )

        future_date = datetime.now() + timedelta(days=1)
        with pytest.raises(ValueError, match="Completion date cannot be in the future"):
            habit.add_completion(future_date)

    def test_completions_sorted(self):
        """Tests that completions are kept sorted (most recent first)."""
        habit = Habit(
            id=1,
            name="Test Habit",
            task="Test Task",
            periodicity=Periodicity.DAILY,
            created_at=datetime.now() - timedelta(days=10),
        )

        # Add completions out of order
        date1 = datetime.now() - timedelta(days=3)
        date2 = datetime.now() - timedelta(days=1)
        date3 = datetime.now() - timedelta(days=2)

        habit.add_completion(date1)
        habit.add_completion(date2)
        habit.add_completion(date3)

        # Should be sorted most recent first
        assert habit.completions[0] == date2
        assert habit.completions[1] == date3
        assert habit.completions[2] == date1

    def test_is_completed_today(self):
        """Tests checking if habit is completed today."""
        habit = Habit(
            id=1,
            name="Test Habit",
            task="Test Task",
            periodicity=Periodicity.DAILY,
            created_at=datetime.now(),
        )

        # Not completed yet
        assert not habit.is_completed_today()

        # Add today's completion
        habit.add_completion(datetime.now())
        assert habit.is_completed_today()

        # Add yesterday's completion
        habit.completions = [datetime.now() - timedelta(days=1)]
        assert not habit.is_completed_today()

    def test_is_completed_this_week(self):
        """Tests checking if habit is completed this week."""
        habit = Habit(
            id=1,
            name="Test Habit",
            task="Test Task",
            periodicity=Periodicity.WEEKLY,
            created_at=datetime.now(),
        )

        # Not completed yet
        assert not habit.is_completed_this_week()

        # Add this week's completion
        habit.add_completion(datetime.now())
        assert habit.is_completed_this_week()

        # Add last week's completion
        habit.completions = [datetime.now() - timedelta(days=8)]
        assert not habit.is_completed_this_week()

    def test_get_streak_daily_no_completions(self):
        """Tests streak calculation for daily habit with no completions."""
        habit = Habit(
            id=1,
            name="Test Habit",
            task="Test Task",
            periodicity=Periodicity.DAILY,
            created_at=datetime.now(),
        )

        assert habit.get_streak() == 0

    def test_get_streak_daily_single_day(self):
        """Test streak calculation for daily habit with today's completion."""
        habit = Habit(
            id=1,
            name="Test Habit",
            task="Test Task",
            periodicity=Periodicity.DAILY,
            created_at=datetime.now(),
        )

        habit.add_completion(datetime.now())
        assert habit.get_streak() == 1

    def test_get_streak_daily_consecutive(self):
        """Tests streak calculation for daily habit with consecutive days."""
        habit = Habit(
            id=1,
            name="Test Habit",
            task="Test Task",
            periodicity=Periodicity.DAILY,
            created_at=datetime.now() - timedelta(days=5),
        )

        # Add consecutive completions
        for i in range(4):
            habit.add_completion(datetime.now() - timedelta(days=i))
        assert habit.get_streak() == 4

    def test_get_streak_daily_broken(self):
        """Tests streak calculation for daily habit with broken streak."""
        habit = Habit(
            id=1,
            name="Test Habit",
            task="Test Task",
            periodicity=Periodicity.DAILY,
            created_at=datetime.now() - timedelta(days=5),
        )

        # Add completions with a gap
        habit.add_completion(datetime.now())  # Today
        habit.add_completion(datetime.now() - timedelta(days=1))  # Yesterday
        # Skip day before yesterday
        habit.add_completion(datetime.now() - timedelta(days=3))  # 3 days ago

        assert habit.get_streak() == 2  # Only today and yesterday count

    def test_get_streak_weekly(self):
        """Tests streak calculation for weekly habit."""
        habit = Habit(
            id=1,
            name="Test Habit",
            task="Test Task",
            periodicity=Periodicity.WEEKLY,
            created_at=datetime.now() - timedelta(weeks=5),
        )

        # Add completions for this week and last week
        habit.add_completion(datetime.now())  # This week
        habit.add_completion(datetime.now() - timedelta(weeks=1))  # Last week

        assert habit.get_streak() == 2
