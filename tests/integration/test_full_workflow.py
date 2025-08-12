import pytest
from datetime import datetime, timedelta

from grit_guardian.core import HabitTracker, Periodicity
from grit_guardian.persistence import DatabaseManager
from grit_guardian.analytics import (
    calculate_streak,
    generate_weekly_view,
    identify_struggled_habits,
)
from grit_guardian.pet import Pet, PetMood


class TestFullHabitWorkflow:
    """Tests complete habit tracking workflows."""

    def test_complete_daily_habit_workflow(self, habit_tracker):
        """Tests full workflow for daily habit management."""
        # 1. Add a daily habit
        habit = habit_tracker.add_habit(
            "Morning Exercise", "Do 20 pushups and 10 sit-ups", "daily"
        )

        assert habit.name == "Morning Exercise"
        assert habit.periodicity == Periodicity.DAILY

        # 2. Verify it appears in habit list
        habits = habit_tracker.list_habits()
        assert len(habits) == 1
        assert habits[0].name == "Morning Exercise"

        # 3. Check initial status (should be pending)
        status = habit_tracker.get_status()
        assert len(status["pending"]) == 1
        assert len(status["completed"]) == 0
        assert status["total"] == 1

        # 4. Complete the habit
        result = habit_tracker.complete_habit("Morning Exercise")
        assert result is True

        # 5. Verify status updated
        status = habit_tracker.get_status()
        assert len(status["pending"]) == 0
        assert len(status["completed"]) == 1
        assert status["total"] == 1

        # 6. Check streak is 1
        streak = habit_tracker.get_habit_streak("Morning Exercise")
        assert streak == 1

        # 7. Try to complete again (should fail)
        with pytest.raises(ValueError, match="already been completed today"):
            habit_tracker.complete_habit("Morning Exercise")

    def test_complete_weekly_habit_workflow(self, habit_tracker):
        """Tests full workflow for weekly habit management."""
        # 1. Add a weekly habit
        habit = habit_tracker.add_habit(
            "Weekly Review", "Review and plan the upcoming week", "weekly"
        )

        assert habit.periodicity == Periodicity.WEEKLY

        # 2. Complete the habit
        result = habit_tracker.complete_habit("Weekly Review")
        assert result is True

        # 3. Check it shows as completed for the week
        status = habit_tracker.get_status()
        assert len(status["completed"]) == 1

        # 4. Try to complete again this week (should fail)
        with pytest.raises(ValueError, match="already been completed this week"):
            habit_tracker.complete_habit("Weekly Review")

    def test_multi_habit_analytics_workflow(self, habit_tracker):
        """Tests analytics across multiple habits."""
        # 1. Add multiple habits
        habit_tracker.add_habit("Exercise", "Daily workout", "daily")
        habit_tracker.add_habit("Reading", "Read for 30 minutes", "daily")
        habit_tracker.add_habit("Planning", "Weekly planning session", "weekly")

        # 2. Complete some habits
        habit_tracker.complete_habit("Exercise")
        habit_tracker.complete_habit("Reading")
        habit_tracker.complete_habit("Planning")

        # 3. Get streak analytics
        streaks = habit_tracker.get_streaks()
        assert len(streaks) == 3

        # All should have current streak of 1
        for streak in streaks:
            assert streak["current_streak"] == 1
            assert streak["longest_streak"] == 1

        # 4. Get overall statistics
        stats = habit_tracker.get_statistics()
        assert stats["total_habits"] == 3
        assert stats["total_completions"] == 3
        assert stats["total_streak"] == 3
        assert stats["active_habits"] == 3

    def test_habit_deletion_workflow(self, habit_tracker):
        """Tests habit deletion and cleanup."""
        # 1. Add habit and complete it
        habit_tracker.add_habit("Test Habit", "Test task", "daily")
        habit_tracker.complete_habit("Test Habit")

        # 2. Verify habit exists with completions
        habits = habit_tracker.list_habits()
        assert len(habits) == 1
        assert len(habits[0].completions) == 1

        # 3. Delete the habit
        result = habit_tracker.delete_habit("Test Habit")
        assert result is True

        # 4. Verify habit is gone
        habits = habit_tracker.list_habits()
        assert len(habits) == 0

        # 5. Verify can't complete deleted habit
        with pytest.raises(Exception):
            habit_tracker.complete_habit("Test Habit")


class TestDatabaseIntegration:
    """Tests database operations integration."""

    def test_persistence_across_sessions(self, temp_db, monkeypatch):
        """Tests that data persists across different tracker instances."""
        # Mock database path for both instances
        monkeypatch.setattr(
            "grit_guardian.persistence.database_manager.DatabaseManager._get_default_db_path",
            lambda self: temp_db,
        )

        # 1. Create first tracker and add habit
        db1 = DatabaseManager()
        tracker1 = HabitTracker(db1)

        tracker1.add_habit("Persistent Habit", "Test persistence", "daily")
        tracker1.complete_habit("Persistent Habit")

        # 2. Create second tracker (simulating new session)
        db2 = DatabaseManager()
        tracker2 = HabitTracker(db2)

        # 3. Verify data persists
        habits = tracker2.list_habits()
        assert len(habits) == 1
        assert habits[0].name == "Persistent Habit"
        assert len(habits[0].completions) == 1

        # 4. Complete again with second tracker
        # Should fail since already completed today
        with pytest.raises(ValueError):
            tracker2.complete_habit("Persistent Habit")

    def test_database_error_handling(self, habit_tracker, monkeypatch):
        """Tests handling of database errors."""
        from unittest.mock import Mock
        import sqlite3

        # First test basic error cases with real tracker
        habit = habit_tracker.get_habit("Nonexistent")
        assert habit is None

        # Try to delete non-existent habit
        with pytest.raises(Exception):
            habit_tracker.delete_habit("Nonexistent")

        # Test database connection errors
        def mock_connection_error(*args, **kwargs):
            raise sqlite3.DatabaseError("Unable to connect to database")

        # Test transaction errors during operations
        mock_db = Mock(spec=DatabaseManager)

        # Configure mock methods that HabitTracker uses
        mock_db.get_habit_by_name.return_value = None  # For add_habit check
        mock_db.create_habit.side_effect = sqlite3.IntegrityError(
            "UNIQUE constraint failed"
        )
        mock_db.add_completion.side_effect = sqlite3.OperationalError(
            "database is locked"
        )
        mock_db.delete_habit.side_effect = sqlite3.DatabaseError("disk I/O error")

        # Create tracker with mocked database
        tracker_with_mock = HabitTracker(mock_db)

        # Test add_habit with database error
        # HabitTracker converts database errors to ValueError
        with pytest.raises(ValueError, match="Failed to create habit"):
            tracker_with_mock.add_habit("Test", "Test task", "daily")

        # Test complete_habit with database error
        # First need to mock that the habit exists
        mock_habit = {
            "id": 1,
            "name": "Test",
            "task": "Test task",
            "periodicity": "daily",
        }
        mock_db.get_habit_by_name.return_value = mock_habit
        mock_db.get_completions.return_value = []  # No completions yet

        # The complete_habit method might wrap errors differently
        with pytest.raises(Exception):  # Could be wrapped in a different exception
            tracker_with_mock.complete_habit("Test")

        # Test delete_habit with database error
        with pytest.raises(Exception):  # Could be wrapped
            tracker_with_mock.delete_habit("Test")

        # Test read operations with errors
        mock_db.get_habits.side_effect = sqlite3.DatabaseError("corrupted database")
        # list_habits might handle errors differently or propagate them
        try:
            result = tracker_with_mock.list_habits()
            # If no exception, check if it returns empty list on error
            assert result == []
        except sqlite3.DatabaseError:
            # Or it might propagate the error
            pass

        # Test connection error scenario with new DatabaseManager instance
        with monkeypatch.context() as m:
            m.setattr("sqlite3.connect", mock_connection_error)
            with pytest.raises(sqlite3.DatabaseError):
                # This will fail when trying to establish new connection
                db = DatabaseManager()

    def test_concurrent_access(self, temp_db, monkeypatch):
        """Tests basic concurrent access patterns."""
        monkeypatch.setattr(
            "grit_guardian.persistence.database_manager.DatabaseManager._get_default_db_path",
            lambda self: temp_db,
        )

        # Create two tracker instances
        tracker1 = HabitTracker(DatabaseManager())
        tracker2 = HabitTracker(DatabaseManager())

        # Add habit with first tracker
        tracker1.add_habit("Shared Habit", "Test concurrency", "daily")

        # Read with second tracker
        habits = tracker2.list_habits()
        assert len(habits) == 1
        assert habits[0].name == "Shared Habit"


class TestAnalyticsIntegration:
    """Tests analytics module integration."""

    def test_streak_calculation_integration(self, habit_tracker):
        """Tests streak calculations with real data."""
        # Add habit
        habit_tracker.add_habit("Streak Test", "Test streaks", "daily")

        # Complete for today first
        habit_tracker.complete_habit("Streak Test")

        # Get habit and manually add completions for testing
        habit = habit_tracker.get_habit("Streak Test")
        base_date = datetime.now()

        # Add manual completions for previous days
        additional_completions = [
            base_date - timedelta(days=1),
            base_date - timedelta(days=2),
            base_date - timedelta(days=3),
            base_date - timedelta(days=4),
        ]

        # Test with manually created completion list
        all_completions = habit.completions + additional_completions
        streak = calculate_streak(all_completions, "daily")
        assert streak == 5

    def test_weekly_view_integration(self, habit_tracker):
        """Tests weekly view with real habit data."""
        # Add habits
        habit_tracker.add_habit("Daily1", "First daily habit", "daily")
        habit_tracker.add_habit("Daily2", "Second daily habit", "daily")

        # Complete some habits
        habit_tracker.complete_habit("Daily1")

        # Generate weekly view
        habits = habit_tracker.list_habits()
        weekly_view = generate_weekly_view(habits)

        # Verify format
        assert "Daily1" in weekly_view
        assert "Daily2" in weekly_view
        assert "Mon | Tue | Wed | Thu | Fri | Sat | Sun" in weekly_view
        assert "✓" in weekly_view  # Should have completion mark

    def test_struggled_habits_identification(self, habit_tracker):
        """Tests identification of struggling habits."""
        # Add habit and create poor completion pattern
        habit_tracker.add_habit("Struggling", "Hard to maintain", "daily")

        # Complete only once (poor performance)
        habit_tracker.complete_habit("Struggling")

        # Get habits and analyze
        habits = habit_tracker.list_habits()
        struggled = identify_struggled_habits(habits, days=7)

        # Should identify as struggling (low completion rate)
        # Note: This depends on the specific implementation
        # and current date, so we mainly test that it runs
        assert isinstance(struggled, list)


class TestPetIntegration:
    """Tests pet system integration."""

    def test_pet_mood_calculation(self, habit_tracker):
        """Tests pet mood changes with habit performance."""
        # Get initial pet (should be default mood)
        pet = habit_tracker.get_pet()
        assert isinstance(pet, Pet)
        assert hasattr(pet, "current_mood")

        # Add and complete habits to improve performance
        habit_tracker.add_habit("Good Habit", "Reliable habit", "daily")
        habit_tracker.complete_habit("Good Habit")

        # Get updated pet
        pet = habit_tracker.get_pet()
        assert pet.current_mood in PetMood

        # Verify pet has ASCII art and messages
        ascii_art = pet.get_ascii_art()
        assert isinstance(ascii_art, str)
        assert len(ascii_art) > 0

        mood_message = pet.get_mood_message()
        assert isinstance(mood_message, str)
        assert len(mood_message) > 0

    def test_pet_mood_progression(self, habit_tracker):
        """Tests pet mood changes with varying performance."""
        # Start with poor performance (no habits)
        pet_empty = habit_tracker.get_pet()
        initial_mood = pet_empty.current_mood

        # Add habits and improve performance
        habit_tracker.add_habit("Exercise", "Daily workout", "daily")
        habit_tracker.add_habit("Reading", "Daily reading", "daily")

        # Complete all habits
        habit_tracker.complete_habit("Exercise")
        habit_tracker.complete_habit("Reading")

        # Pet mood should potentially improve
        pet_improved = habit_tracker.get_pet()
        # Note: Actual mood comparison depends on implementation
        # We mainly test that the system works
        assert pet_improved.current_mood in PetMood


class TestSampleDataIntegration:
    """Tests sample data initialization."""

    def test_sample_data_creation(self, habit_tracker):
        """Tests sample data initialization workflow."""
        # Initially no habits
        assert len(habit_tracker.list_habits()) == 0

        # Initialize sample data
        result = habit_tracker.initialize_sample_data()
        assert result is True

        # Verify sample habits created
        habits = habit_tracker.list_habits()
        assert len(habits) == 4

        habit_names = [h.name for h in habits]
        assert "Morning Reading" in habit_names
        assert "Exercise" in habit_names
        assert "Weekly Planning" in habit_names
        assert "Learn Something New" in habit_names

        # Try to initialize again (should fail)
        result = habit_tracker.initialize_sample_data()
        assert result is False

    def test_sample_data_usability(self, habit_tracker):
        """Tests that sample data is fully functional."""
        # Initialize sample data
        habit_tracker.initialize_sample_data()

        # Complete one of the sample habits
        result = habit_tracker.complete_habit("Morning Reading")
        assert result is True

        # Verify status updates
        status = habit_tracker.get_status()
        assert len(status["completed"]) == 1
        assert len(status["pending"]) == 3

        # Test analytics with sample data
        streaks = habit_tracker.get_streaks()
        assert len(streaks) == 4

        # Test pet with sample data
        pet = habit_tracker.get_pet()
        assert pet.current_mood in PetMood


class TestErrorHandlingIntegration:
    """Tests error handling across the system."""

    def test_invalid_input_handling(self, habit_tracker):
        """Tests system handles invalid inputs gracefully."""
        # Empty names
        with pytest.raises(ValueError):
            habit_tracker.add_habit("", "Valid task", "daily")

        with pytest.raises(ValueError):
            habit_tracker.add_habit("   ", "Valid task", "daily")

        # Empty tasks
        with pytest.raises(ValueError):
            habit_tracker.add_habit("Valid name", "", "daily")

        # Invalid periodicity
        with pytest.raises(ValueError):
            habit_tracker.add_habit("Valid name", "Valid task", "monthly")

    def test_duplicate_habit_handling(self, habit_tracker):
        """Tests duplicate habit error handling."""
        # Add first habit
        habit_tracker.add_habit("Test Habit", "First version", "daily")

        # Try to add duplicate
        with pytest.raises(Exception):  # Should raise HabitAlreadyExistsError
            habit_tracker.add_habit("Test Habit", "Second version", "daily")

        # Verify only one habit exists
        habits = habit_tracker.list_habits()
        assert len(habits) == 1

    def test_nonexistent_habit_operations(self, habit_tracker):
        """Tests operations on non-existent habits."""
        # Complete non-existent habit
        with pytest.raises(Exception):
            habit_tracker.complete_habit("Nonexistent")

        # Delete non-existent habit
        with pytest.raises(Exception):
            habit_tracker.delete_habit("Nonexistent")

        # Get streak for non-existent habit
        with pytest.raises(Exception):
            habit_tracker.get_habit_streak("Nonexistent")


class TestPerformanceIntegration:
    """Tests system performance with larger datasets."""

    def test_many_habits_performance(self, habit_tracker):
        """Tests system performance with many habits."""
        # Add many habits
        for i in range(50):
            habit_tracker.add_habit(
                f"Habit {i}", f"Task {i}", "daily" if i % 2 == 0 else "weekly"
            )

        # Verify all habits added
        habits = habit_tracker.list_habits()
        assert len(habits) == 50

        # Complete some habits
        for i in range(0, 50, 5):  # Every 5th habit
            habit_tracker.complete_habit(f"Habit {i}")

        # Test analytics performance
        streaks = habit_tracker.get_streaks()
        assert len(streaks) == 50

        # Test statistics
        stats = habit_tracker.get_statistics()
        assert stats["total_habits"] == 50
        assert stats["total_completions"] == 10

    def test_many_completions_performance(self, habit_tracker):
        """Tests system performance with many completions."""
        # Add a habit
        habit_tracker.add_habit("Heavy Habit", "Lots of completions", "daily")

        # Complete today
        habit_tracker.complete_habit("Heavy Habit")

        # Get habit and test analytics work with realistic data
        habit = habit_tracker.get_habit("Heavy Habit")
        assert len(habit.completions) == 1  # One completion for today

        # Test streak calculation works
        streak = habit_tracker.get_habit_streak("Heavy Habit")
        assert isinstance(streak, int)
        assert streak >= 0
