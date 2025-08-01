from datetime import datetime, timedelta, date
from typing import TYPE_CHECKING, List, Dict, Any

# Avoid circular imports
# https://docs.python.org/3/library/typing.html#typing.TYPE_CHECKING
if TYPE_CHECKING:
    from ..core.models import Habit


def calculate_streak(completions: List[datetime], periodicity: str) -> int:
    """Calculates current streak for a habit.

    Args:
        completions: List of completion datetime objects
        periodicity: Either 'daily' or 'weekly'

    Returns:
        Current streak count
    """
    pass


def calculate_longest_streak(completions: List[datetime], periodicity: str) -> int:
    """Finds the longest streak ever achieved.

    Uses a functional approach to calculate streaks.

    Args:
        completions: List of completion datetime objects
        periodicity: Either 'daily' or 'weekly'

    Returns:
        Longest streak count
    """
    pass


def get_completion_rate(
    habit_created: datetime, completions: List[datetime], periodicity: str
) -> float:
    """Calculates percentage of successful completions.

    Args:
        habit_created: When the habit was created
        completions: List of completion datetime objects
        periodicity: Either 'daily' or 'weekly'

    Returns:
        Completion rate as a percentage (0.0 to 100.0)
    """
    pass


def get_habit_analytics(
    habit_name: str, created_at: datetime, completions: List[datetime], periodicity: str
) -> Dict[str, Any]:
    """Gets analytics for a single habit.

    Args:
        habit_name: Name of the habit
        created_at: When the habit was created
        completions: List of completion datetime objects
        periodicity: Either 'daily' or 'weekly'

    Returns:
        Dictionary containing all analytics metrics
    """
    pass


def generate_weekly_view(habits: List["Habit"]) -> str:
    """Generates ASCII table for weekly progress.

    Args:
        habits: List of Habit objects to display

    Returns:
        String containing formatted ASCII table
    """
    pass


def calculate_expected_completions(habit: "Habit", since_date: datetime) -> int:
    """Calculates expected number of completions for a habit since a given date.

    Args:
        habit: Habit object
        since_date: Date to calculate from

    Returns:
        Expected number of completions
    """
    pass


def identify_struggled_habits(habits: List["Habit"], days: int = 30) -> List[Dict]:
    """Finds habits with low completion rates in given period.

    Args:
        habits: List of Habit objects to analyze
        days: Number of days to look back (default: 30)

    Returns:
        List of dictionaries with struggling habit information
    """
    pass
