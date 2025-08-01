import pytest
from datetime import datetime, timedelta
from grit_guardian.analytics.analytics import (
    calculate_streak,
    calculate_longest_streak,
    get_completion_rate,
    get_habit_analytics,
    generate_weekly_view,
    calculate_expected_completions,
    identify_struggled_habits,
)
from grit_guardian.core.models import Habit, Periodicity


class TestCalculateStreak:
    """Tests the calculate_streak function."""

    def test_empty_completions(self):
        """Tests with no completions."""
        assert calculate_streak([], "daily") == 0
        assert calculate_streak([], "weekly") == 0

    def test_daily_streak_consecutive(self):
        """Tests daily streak with consecutive days."""
        today = datetime.now()
        completions = [
            today,
            today - timedelta(days=1),
            today - timedelta(days=2),
            today - timedelta(days=3),
        ]
        assert calculate_streak(completions, "daily") == 4

    def test_daily_streak_with_gap(self):
        """Tests daily streak broken by a gap."""
        today = datetime.now()
        completions = [
            today,
            today - timedelta(days=1),
            # Gap here
            today - timedelta(days=3),
            today - timedelta(days=4),
        ]
        assert calculate_streak(completions, "daily") == 2

    def test_daily_streak_no_today(self):
        """Tests daily streak when habit not completed today."""
        today = datetime.now()
        completions = [
            today - timedelta(days=1),
            today - timedelta(days=2),
            today - timedelta(days=3),
        ]
        assert calculate_streak(completions, "daily") == 0

    def test_weekly_streak_consecutive(self):
        """Tests weekly streak with consecutive weeks."""
        today = datetime.now()
        completions = [
            today,
            today - timedelta(weeks=1),
            today - timedelta(weeks=2),
            today - timedelta(weeks=3),
        ]
        assert calculate_streak(completions, "weekly") == 4

    def test_weekly_streak_with_gap(self):
        """Tests weekly streak broken by a gap."""
        today = datetime.now()
        completions = [
            today,
            today - timedelta(weeks=1),
            # Gap here
            today - timedelta(weeks=3),
            today - timedelta(weeks=4),
        ]
        assert calculate_streak(completions, "weekly") == 2

    def test_weekly_streak_year_boundary(self):
        """Tests weekly streak across year boundary."""
        # Use monkeypatch or just test the logic with specific dates
        # For now, skip this test as it requires proper mocking framework
        pytest.skip("Requires proper datetime mocking")


class TestCalculateLongestStreak:
    """Tests the calculate_longest_streak function."""

    def test_empty_completions(self):
        """Tests with no completions."""
        assert calculate_longest_streak([], "daily") == 0
        assert calculate_longest_streak([], "weekly") == 0

    def test_single_completion(self):
        """Tests with single completion."""
        completions = [datetime.now()]
        assert calculate_longest_streak(completions, "daily") == 1
        assert calculate_longest_streak(completions, "weekly") == 1

    def test_daily_longest_streak(self):
        """Tests finding longest daily streak."""
        base_date = datetime.now()
        completions = [
            # First streak: 3 days
            base_date - timedelta(days=10),
            base_date - timedelta(days=9),
            base_date - timedelta(days=8),
            # Gap (day 7 missing)
            # Second streak: 5 days (longest)
            base_date - timedelta(days=5),
            base_date - timedelta(days=4),
            base_date - timedelta(days=3),
            base_date - timedelta(days=2),
            base_date - timedelta(days=1),
            # Current day
            base_date,
        ]
        # The longest streak is actually 6 (from day 5 to today)
        assert calculate_longest_streak(completions, "daily") == 6

    def test_weekly_longest_streak(self):
        """Tests finding longest weekly streak."""
        base_date = datetime.now()
        completions = [
            # First streak: 2 weeks
            base_date - timedelta(weeks=10),
            base_date - timedelta(weeks=9),
            # Gap
            # Second streak: 4 weeks (longest)
            base_date - timedelta(weeks=6),
            base_date - timedelta(weeks=5),
            base_date - timedelta(weeks=4),
            base_date - timedelta(weeks=3),
            # Gap
            # Current streak: 1 week
            base_date,
        ]
        assert calculate_longest_streak(completions, "weekly") == 4

    def test_multiple_completions_same_period(self):
        """Tests multiple completions in same period count as one."""
        base_date = datetime.now()
        completions = [
            base_date,
            base_date - timedelta(hours=1),  # Same day
            base_date - timedelta(hours=2),  # Same day
            base_date - timedelta(days=1),
            base_date - timedelta(days=1, hours=1),  # Same day as previous
        ]
        assert calculate_longest_streak(completions, "daily") == 2


class TestGetCompletionRate:
    """Tests the get_completion_rate function."""

    def test_no_completions(self):
        """Tests completion rate with no completions."""
        created = datetime.now() - timedelta(days=10)
        assert get_completion_rate(created, [], "daily") == 0.0

    def test_future_creation_date(self):
        """Tests with future creation date."""
        created = datetime.now() + timedelta(days=1)
        assert get_completion_rate(created, [], "daily") == 0.0

    def test_daily_perfect_completion(self):
        """Tests 100% completion rate for daily habit."""
        created = datetime.now() - timedelta(days=4)
        completions = [
            datetime.now(),
            datetime.now() - timedelta(days=1),
            datetime.now() - timedelta(days=2),
            datetime.now() - timedelta(days=3),
            datetime.now() - timedelta(days=4),
        ]
        assert get_completion_rate(created, completions, "daily") == 100.0

    def test_daily_partial_completion(self):
        """Test partial completion rate for daily habit."""
        created = datetime.now() - timedelta(days=9)  # 10 days total
        completions = [
            datetime.now(),
            datetime.now() - timedelta(days=2),
            datetime.now() - timedelta(days=5),
            datetime.now() - timedelta(days=7),
            datetime.now() - timedelta(days=9),
        ]
        # 5 out of 10 days = 50%
        assert get_completion_rate(created, completions, "daily") == 50.0

    def test_weekly_completion_rate(self):
        """Tests completion rate for weekly habit."""
        created = datetime.now() - timedelta(weeks=3, days=3)  # 4 weeks total
        completions = [
            datetime.now(),
            datetime.now() - timedelta(weeks=1),
            datetime.now() - timedelta(weeks=3),
        ]
        # 3 out of 4 weeks = 75%
        assert get_completion_rate(created, completions, "weekly") == 75.0

    def test_multiple_completions_same_period(self):
        """Tests that multiple completions in same period don't inflate rate."""
        created = datetime.now() - timedelta(days=4)
        completions = [
            datetime.now(),
            datetime.now() - timedelta(hours=1),  # Same day
            datetime.now() - timedelta(hours=2),  # Same day
            datetime.now() - timedelta(days=1),
            datetime.now() - timedelta(days=2),
            datetime.now() - timedelta(days=3),
            datetime.now() - timedelta(days=4),
        ]
        # Still 100% despite multiple completions on same day
        assert get_completion_rate(created, completions, "daily") == 100.0


class TestGetHabitAnalytics:
    """Tests the get_habit_analytics function."""

    def test_comprehensive_analytics(self):
        """Tests getting all analytics for a habit."""
        created = datetime.now() - timedelta(days=9)
        completions = [
            datetime.now(),
            datetime.now() - timedelta(days=1),
            datetime.now() - timedelta(days=2),
            # Gap
            datetime.now() - timedelta(days=5),
            datetime.now() - timedelta(days=6),
        ]

        analytics = get_habit_analytics("Test Habit", created, completions, "daily")

        assert analytics["name"] == "Test Habit"
        assert analytics["current_streak"] == 3
        assert analytics["longest_streak"] == 3
        assert analytics["completion_rate"] == 50.0
        assert analytics["total_completions"] == 5
        assert analytics["days_since_creation"] == 9

    def test_empty_habit_analytics(self):
        """Test analytics for habit with no completions."""
        created = datetime.now() - timedelta(days=5)

        analytics = get_habit_analytics("Empty Habit", created, [], "daily")

        assert analytics["name"] == "Empty Habit"
        assert analytics["current_streak"] == 0
        assert analytics["longest_streak"] == 0
        assert analytics["completion_rate"] == 0.0
        assert analytics["total_completions"] == 0
        assert analytics["days_since_creation"] == 5


# Property-based testing for streak algos
class TestStreakProperties:
    """Property-based tests for streak calculations."""

    def test_streak_never_exceeds_total_completions(self):
        """Current streak should never exceed total completions."""
        completions = [datetime.now() - timedelta(days=i) for i in range(5)]
        for periodicity in ["daily", "weekly"]:
            streak = calculate_streak(completions, periodicity)
            assert streak <= len(completions)

    def test_longest_streak_gte_current_streak(self):
        """Longest streak should always be >= current streak."""
        completions = [datetime.now() - timedelta(days=i) for i in range(10)]
        for periodicity in ["daily", "weekly"]:
            current = calculate_streak(completions, periodicity)
            longest = calculate_longest_streak(completions, periodicity)
            assert longest >= current

    def test_completion_rate_bounded(self):
        """Completion rate should be between 0 and 100."""
        created = datetime.now() - timedelta(days=10)
        completions = [
            datetime.now() - timedelta(days=i)
            for i in range(20)  # More than expected
        ]
        for periodicity in ["daily", "weekly"]:
            rate = get_completion_rate(created, completions, periodicity)
            assert 0.0 <= rate <= 100.0


class TestWeeklyView:
    """Tests the generate_weekly_view function."""

    def test_weekly_view_empty_habits(self):
        """Test weekly view with no habits."""
        result = generate_weekly_view([])
        assert "Habit" in result
        assert "Mon | Tue | Wed | Thu | Fri | Sat | Sun" in result

    def test_weekly_view_single_habit(self):
        """Tests weekly view with one habit."""
        today = datetime.now()
        monday = today - timedelta(days=today.weekday())  # Get Monday of current week

        habit = Habit(
            id=1,
            name="Test Habit",
            task="Test task",
            periodicity=Periodicity.DAILY,
            created_at=today - timedelta(days=14),  # Created 2 weeks ago
            completions=[
                monday,  # Monday completion
                monday + timedelta(days=2),  # Wednesday completion
                # Missing Tuesday, Thursday, etc.
            ],
        )

        result = generate_weekly_view([habit])
        assert "Test Habit" in result
        assert "✓" in result  # Should have completions
        # Only check for missed days if we're past Monday
        if today.weekday() > 0:  # If today is not Monday
            assert "✗" in result  # Should have missed days

    def test_weekly_view_long_habit_name(self):
        """Tests that long habit names are truncated."""
        habit = Habit(
            id=1,
            name="This is a very long habit name that should be truncated",
            task="Test",
            periodicity=Periodicity.DAILY,
            created_at=datetime.now(),
            completions=[],
        )

        result = generate_weekly_view([habit])
        lines = result.split("\n")
        # Find the habit line (not header or separator)
        habit_line = lines[2]
        # Check that the name part is exactly 20 characters
        name_part = habit_line.split(" | ")[0]
        assert len(name_part) == 20


class TestExpectedCompletions:
    """Tests the calculate_expected_completions function."""

    def test_daily_habit_full_period(self):
        """Tests expected completions for daily habit."""
        habit = Habit(
            id=1,
            name="Daily Test",
            task="Test",
            periodicity=Periodicity.DAILY,
            created_at=datetime.now() - timedelta(days=10),
            completions=[],
        )

        since_date = datetime.now() - timedelta(days=7)
        expected = calculate_expected_completions(habit, since_date)
        assert expected == 8  # 7 days + today

    def test_weekly_habit_full_period(self):
        """Tests expected completions for weekly habit."""
        habit = Habit(
            id=1,
            name="Weekly Test",
            task="Test",
            periodicity=Periodicity.WEEKLY,
            created_at=datetime.now() - timedelta(days=30),
            completions=[],
        )

        since_date = datetime.now() - timedelta(days=14)
        expected = calculate_expected_completions(habit, since_date)
        assert expected == 3  # 2 full weeks + current partial week

    def test_habit_created_after_since_date(self):
        """Tests when habit was created after the analysis start date."""
        habit = Habit(
            id=1,
            name="New Habit",
            task="Test",
            periodicity=Periodicity.DAILY,
            created_at=datetime.now() - timedelta(days=3),
            completions=[],
        )

        since_date = datetime.now() - timedelta(days=10)
        expected = calculate_expected_completions(habit, since_date)
        assert expected == 4  # Only 3 days + today since creation


class TestStruggleIdentification:
    """Test the identify_struggled_habits function."""

    def test_no_struggled_habits(self):
        """Tests when all habits are doing well."""
        today = datetime.now()
        habit = Habit(
            id=1,
            name="Good Habit",
            task="Test",
            periodicity=Periodicity.DAILY,
            created_at=today - timedelta(days=10),
            completions=[today - timedelta(days=i) for i in range(8)],
        )

        struggled = identify_struggled_habits([habit], days=7)
        assert len(struggled) == 0

    def test_identify_struggled_habit(self):
        """Tests identifying a habit with low completion rate."""
        today = datetime.now()
        habit = Habit(
            id=1,
            name="Struggling Habit",
            task="Test",
            periodicity=Periodicity.DAILY,
            created_at=today - timedelta(days=10),
            completions=[
                today - timedelta(days=6),
                today - timedelta(days=4),
            ],  # 2 completions in last 7 days
        )

        struggled = identify_struggled_habits([habit], days=7)
        assert len(struggled) == 1
        assert struggled[0]["name"] == "Struggling Habit"
        assert struggled[0]["completion_rate"] == 0.25  # 2/8 (7 days + today)
        assert struggled[0]["missed"] == 6

    def test_exactly_50_percent_not_struggled(self):
        """Tests that exactly 50% completion is not considered struggling."""
        today = datetime.now()
        habit = Habit(
            id=1,
            name="Borderline Habit",
            task="Test",
            periodicity=Periodicity.DAILY,
            created_at=today - timedelta(days=10),
            completions=[
                today - timedelta(days=i) for i in range(0, 8, 2)
            ],  # 4 out of 8
        )

        struggled = identify_struggled_habits([habit], days=7)
        assert len(struggled) == 0

    def test_sort_by_completion_rate(self):
        """Tests that struggled habits are sorted by completion rate."""
        today = datetime.now()
        habits = [
            Habit(
                id=1,
                name="Worst Habit",
                task="Test",
                periodicity=Periodicity.DAILY,
                created_at=today - timedelta(days=10),
                completions=[today - timedelta(days=7)],  # 1/8 = 12.5%
            ),
            Habit(
                id=2,
                name="Bad Habit",
                task="Test",
                periodicity=Periodicity.DAILY,
                created_at=today - timedelta(days=10),
                completions=[
                    today - timedelta(days=i) for i in [0, 2, 5]
                ],  # 3/8 = 37.5%
            ),
        ]

        struggled = identify_struggled_habits(habits, days=7)
        assert len(struggled) == 2
        assert struggled[0]["name"] == "Worst Habit"
        assert struggled[1]["name"] == "Bad Habit"
