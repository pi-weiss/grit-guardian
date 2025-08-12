import pytest
from unittest.mock import Mock
from datetime import datetime, timedelta

from grit_guardian.core import (
    HabitAlreadyExistsError,
    HabitTracker,
    HabitNotFoundError,
)
from grit_guardian.core import Periodicity


class TestHabitTracker:
    """Tests the HabitTracker service."""

    @pytest.fixture
    def mock_db(self):
        """Creates a mock DatabaseManager."""
        # Use mock object to separate from direct database operations
        # https://docs.python.org/3/library/unittest.mock.html
        return Mock()

    @pytest.fixture
    def tracker(self, mock_db):
        """Creates a HabitTracker instance with mock database."""
        return HabitTracker(mock_db)

    def test_init(self, mock_db):
        """Tests HabitTracker initialization."""
        tracker = HabitTracker(mock_db)
        assert tracker.db is mock_db

    def test_add_habit_success(self, tracker, mock_db):
        """Tests successfully adding a new habit."""
        # Setup mock
        mock_db.get_habit_by_name.return_value = None  # Habit doesn't exist
        mock_db.create_habit.return_value = 1  # Return habit id

        # Add habit
        habit = tracker.add_habit("Morning Exercise", "Do 20 pushups", "daily")

        # Verify
        assert habit.id == 1
        assert habit.name == "Morning Exercise"
        assert habit.task == "Do 20 pushups"
        assert habit.periodicity == Periodicity.DAILY
        assert habit.completions == []

        # Verify database calls
        mock_db.get_habit_by_name.assert_called_once_with("Morning Exercise")
        mock_db.create_habit.assert_called_once_with(
            "Morning Exercise", "Do 20 pushups", "daily"
        )

    def test_add_habit_empty_name(self, tracker):
        """Test adding habit with empty name raises ValueError."""
        with pytest.raises(ValueError, match="Habit name cannot be empty"):
            tracker.add_habit("", "Test task", "daily")

    def test_add_habit_whitespace_name(self, tracker):
        """Test adding habit with whitespace name raises ValueError."""
        with pytest.raises(ValueError, match="Habit name cannot be empty"):
            tracker.add_habit("  ", "Test task", "daily")

    def test_add_habit_empty_task(self, tracker):
        """Test adding habit with empty task raises ValueError."""
        with pytest.raises(ValueError, match="Habit task cannot be empty"):
            tracker.add_habit("Test habit", "", "daily")

    def test_add_habit_invalid_periodicity(self, tracker):
        """Test adding habit with invalid periodicity raises ValueError."""
        with pytest.raises(ValueError, match="Invalid periodicity"):
            tracker.add_habit("Test habit", "Test task", "monthly")

    def test_add_habit_already_exists(self, tracker, mock_db):
        """Test adding habit that already exists raises HabitAlreadyExistsError."""
        # Setup mock - habit already exists
        mock_db.get_habit_by_name.return_value = {"id": 1, "name": "Exercise"}

        with pytest.raises(HabitAlreadyExistsError, match="already exists"):
            tracker.add_habit("Exercise", "Do pushups", "daily")

    def test_add_habit_database_error(self, tracker, mock_db):
        """Tests handling database error during habit creation."""
        # Setup mock
        mock_db.get_habit_by_name.return_value = None
        mock_db.create_habit.side_effect = Exception("Database error")

        with pytest.raises(ValueError, match="Failed to create habit"):
            tracker.add_habit("Test habit", "Test task", "daily")

    def test_list_habits_empty(self, tracker, mock_db):
        """Test listing habits when none exist."""
        mock_db.get_habits.return_value = []

        habits = tracker.list_habits()
        assert habits == []

    def test_list_habits_with_data(self, tracker, mock_db):
        """Tests listing habits with data."""
        # Setup mock
        created_at = datetime.now()
        mock_db.get_habits.return_value = [
            {
                "id": 1,
                "name": "Exercise",
                "task": "Do pushups",
                "periodicity": "daily",
                "created_at": created_at,
                "total_completions": 2,
                "last_completed": datetime.now(),
            },
            {
                "id": 2,
                "name": "Read",
                "task": "Read 10 pages",
                "periodicity": "weekly",
                "created_at": created_at,
                "total_completions": 0,
                "last_completed": None,
            },
        ]

        completion_dates = [datetime.now(), datetime.now() - timedelta(days=1)]
        mock_db.get_completions.return_value = completion_dates

        # Get habits
        habits = tracker.list_habits()

        # Verify
        assert len(habits) == 2
        assert habits[0].name == "Exercise"
        assert habits[0].completions == completion_dates
        assert habits[1].name == "Read"
        assert habits[1].completions == []

        # Verify database calls
        mock_db.get_completions.assert_called_once_with("Exercise")

    def test_get_habit_found(self, tracker, mock_db):
        """Tests getting a specific habit that exists."""
        # Setup mock
        created_at = datetime.now()
        mock_db.get_habit_by_name.return_value = {
            "id": 1,
            "name": "Exercise",
            "task": "Do pushups",
            "periodicity": "daily",
            "created_at": created_at,
        }

        completion_dates = [datetime.now(), datetime.now() - timedelta(days=1)]
        mock_db.get_completions.return_value = completion_dates

        # Get habit
        habit = tracker.get_habit("Exercise")

        # Verify
        assert habit is not None
        assert habit.name == "Exercise"
        assert habit.completions == completion_dates

        # Verify database calls
        mock_db.get_habit_by_name.assert_called_once_with("Exercise")
        mock_db.get_completions.assert_called_once_with("Exercise")

    def test_get_habit_not_found(self, tracker, mock_db):
        """Tests getting a habit that doesn't exist."""
        mock_db.get_habit_by_name.return_value = None

        habit = tracker.get_habit("NonExistent")
        assert habit is None

    def test_delete_habit_success(self, tracker, mock_db):
        """Tests successfully deleting a habit."""
        # Setup mock
        mock_db.get_habit_by_name.return_value = {"id": 1, "name": "Exercise"}
        mock_db.delete_habit.return_value = True

        # Delete habit
        result = tracker.delete_habit("Exercise")

        # Verify
        assert result is True
        mock_db.get_habit_by_name.assert_called_once_with("Exercise")
        mock_db.delete_habit.assert_called_once_with("Exercise")

    def test_delete_habit_not_found(self, tracker, mock_db):
        """Tests deleting a habit that doesn't exist."""
        mock_db.get_habit_by_name.return_value = None

        with pytest.raises(HabitNotFoundError, match="not found"):
            tracker.delete_habit("NonExistent")

    def test_complete_habit_success(self, tracker, mock_db):
        """Tests successfully completing a habit."""
        # Setup mock - habit exists and not completed today
        created_at = datetime.now() - timedelta(days=5)
        mock_db.get_habit_by_name.return_value = {
            "id": 1,
            "name": "Exercise",
            "task": "Do pushups",
            "periodicity": "daily",
            "created_at": created_at,
        }
        mock_db.get_completions.return_value = [datetime.now() - timedelta(days=1)]
        mock_db.add_completion.return_value = 1

        # Complete habit
        result = tracker.complete_habit("Exercise")

        # Verify
        assert result is True
        mock_db.add_completion.assert_called_once()

    def test_complete_habit_not_found(self, tracker, mock_db):
        """Tests completing a habit that doesn't exist."""
        mock_db.get_habit_by_name.return_value = None

        with pytest.raises(HabitNotFoundError, match="not found"):
            tracker.complete_habit("NonExistent")

    def test_complete_habit_already_completed_daily(self, tracker, mock_db):
        """Tests completing a daily habit that's already completed today."""
        # Setup mock - habit completed today
        created_at = datetime.now() - timedelta(days=5)
        mock_db.get_habit_by_name.return_value = {
            "id": 1,
            "name": "Exercise",
            "task": "Do pushups",
            "periodicity": "daily",
            "created_at": created_at,
        }
        mock_db.get_completions.return_value = [datetime.now()]  # Completed today

        with pytest.raises(ValueError, match="already been completed today"):
            tracker.complete_habit("Exercise")

    def test_complete_habit_already_completed_weekly(self, tracker, mock_db):
        """Tests completing a weekly habit that's already completed this week."""
        # Setup mock - habit completed this week
        created_at = datetime.now() - timedelta(weeks=5)
        mock_db.get_habit_by_name.return_value = {
            "id": 1,
            "name": "Review",
            "task": "Weekly review",
            "periodicity": "weekly",
            "created_at": created_at,
        }
        mock_db.get_completions.return_value = [datetime.now()]  # Completed this week

        with pytest.raises(ValueError, match="already been completed this week"):
            tracker.complete_habit("Review")

    def test_complete_habit_database_error(self, tracker, mock_db):
        """Tests handling database error during completion."""
        # Setup mock
        created_at = datetime.now() - timedelta(days=5)
        mock_db.get_habit_by_name.return_value = {
            "id": 1,
            "name": "Exercise",
            "task": "Do pushups",
            "periodicity": "daily",
            "created_at": created_at,
        }
        mock_db.get_completions.return_value = []
        mock_db.add_completion.side_effect = ValueError("Database error")

        with pytest.raises(ValueError, match="Failed to complete habit"):
            tracker.complete_habit("Exercise")

    def test_get_habit_streak(self, tracker, mock_db):
        """Tests getting habit streak."""
        # Setup mock
        created_at = datetime.now() - timedelta(days=5)
        mock_db.get_habit_by_name.return_value = {
            "id": 1,
            "name": "Exercise",
            "task": "Do pushups",
            "periodicity": "daily",
            "created_at": created_at,
        }

        # Three consecutive days
        completions = [
            datetime.now(),
            datetime.now() - timedelta(days=1),
            datetime.now() - timedelta(days=2),
        ]
        mock_db.get_completions.return_value = completions

        # Get streak
        streak = tracker.get_habit_streak("Exercise")
        assert streak == 3

    def test_get_habit_streak_not_found(self, tracker, mock_db):
        """Tests getting streak for non-existent habit."""
        mock_db.get_habit_by_name.return_value = None

        with pytest.raises(HabitNotFoundError, match="not found"):
            tracker.get_habit_streak("NonExistent")

    def test_get_statistics(self, tracker, mock_db):
        """Tests getting overall statistics."""
        # Setup mock database stats
        mock_db.get_stats.return_value = {
            "total_habits": 3,
            "total_completions": 10,
            "habits_by_periodicity": {"daily": 2, "weekly": 1},
        }

        # Setup mock habits for streak calculation
        created_at = datetime.now() - timedelta(days=10)
        mock_db.get_habits.return_value = [
            {
                "id": 1,
                "name": "Exercise",
                "task": "Do pushups",
                "periodicity": "daily",
                "created_at": created_at,
                "total_completions": 5,
                "last_completed": datetime.now(),
            },
            {
                "id": 2,
                "name": "Read",
                "task": "Read 10 pages",
                "periodicity": "daily",
                "created_at": created_at,
                "total_completions": 3,
                "last_completed": datetime.now(),
            },
        ]

        # Mock completions for streak calculation
        exercise_completions = [
            datetime.now(),
            datetime.now() - timedelta(days=1),
            datetime.now() - timedelta(days=2),
        ]
        read_completions = [datetime.now(), datetime.now() - timedelta(days=1)]

        mock_db.get_completions.side_effect = [exercise_completions, read_completions]

        # Get statistics
        stats = tracker.get_statistics()

        # Verify basic stats
        assert stats["total_habits"] == 3
        assert stats["total_completions"] == 10
        assert stats["habits_by_periodicity"] == {"daily": 2, "weekly": 1}

        # Verify calculated stats
        assert stats["total_streak"] == 5  # 3 + 2
        assert stats["longest_streak"] == 3
        assert stats["longest_streak_habit"] == "Exercise"
        assert stats["active_habits"] == 2
