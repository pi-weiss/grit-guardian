import pytest
import tempfile
from pathlib import Path
from unittest.mock import Mock
from datetime import datetime, timedelta

from grit_guardian.persistence.database_manager import DatabaseManager
from grit_guardian.core.models import Habit, Periodicity
from grit_guardian.core.habit_tracker import HabitTracker


@pytest.fixture
def mock_db():
    """Creates a mock DatabaseManager for unit testing.

    Returns:
        Mock DatabaseManager instance
    """
    mock = Mock(spec=DatabaseManager)
    # Set up common return values
    mock.get_habits.return_value = []
    mock.get_stats.return_value = {
        "total_habits": 0,
        "total_completions": 0,
        "habits_by_periodicity": {"daily": 0, "weekly": 0},
    }
    return mock


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


@pytest.fixture
def db_manager(temp_db):
    """Creates DatabaseManager with test database.

    Args:
        temp_db: Temporary database path fixture

    Returns:
        DatabaseManager instance using test database
    """
    return DatabaseManager(db_path=temp_db)


@pytest.fixture
def habit_tracker(db_manager):
    """Creates HabitTracker with test database.

    Args:
        db_manager: DatabaseManager fixture

    Returns:
        HabitTracker instance
    """
    return HabitTracker(db_manager)


@pytest.fixture
def mock_tracker(mock_db):
    """Creates HabitTracker with mock database.

    Args:
        mock_db: Mock DatabaseManager fixture

    Returns:
        HabitTracker instance with mocked database
    """
    return HabitTracker(mock_db)


@pytest.fixture
def sample_habit():
    """Creates a sample Habit instance for testing.

    Returns:
        Habit instance with test data
    """
    return Habit(
        id=1,
        name="Test Exercise",
        task="Do 20 pushups",
        periodicity=Periodicity.DAILY,
        created_at=datetime.now() - timedelta(days=7),
        completions=[
            datetime.now(),
            datetime.now() - timedelta(days=1),
            datetime.now() - timedelta(days=2),
        ],
    )


@pytest.fixture
def sample_habits():
    """Creates multiple sample habits for testing.

    Returns:
        List of Habit instances with varied data
    """
    base_date = datetime.now()
    return [
        Habit(
            id=1,
            name="Morning Reading",
            task="Read for 15 minutes",
            periodicity=Periodicity.DAILY,
            created_at=base_date - timedelta(days=14),
            completions=[
                base_date,
                base_date - timedelta(days=1),
                base_date - timedelta(days=2),
                base_date - timedelta(days=4),
            ],
        ),
        Habit(
            id=2,
            name="Exercise",
            task="Physical activity for 30 minutes",
            periodicity=Periodicity.DAILY,
            created_at=base_date - timedelta(days=10),
            completions=[
                base_date,
                base_date - timedelta(days=1),
                base_date - timedelta(days=2),
                base_date - timedelta(days=3),
                base_date - timedelta(days=4),
            ],
        ),
        Habit(
            id=3,
            name="Weekly Planning",
            task="Review and plan upcoming week",
            periodicity=Periodicity.WEEKLY,
            created_at=base_date - timedelta(weeks=6),
            completions=[
                base_date - timedelta(weeks=0, days=2),
                base_date - timedelta(weeks=1, days=3),
                base_date - timedelta(weeks=3, days=1),
            ],
        ),
    ]


@pytest.fixture
def mock_datetime(monkeypatch):
    """Mocks datetime.now() for consistent testing.

    Args:
        monkeypatch: Pytest monkeypatch fixture

    Returns:
        Function to set the mocked datetime
    """

    class MockDatetime:
        _now = None

        @classmethod
        def now(cls):
            return cls._now or datetime.now()

        @classmethod
        def set_now(cls, dt):
            cls._now = dt

    monkeypatch.setattr("grit_guardian.core.habit_tracker.datetime", MockDatetime)
    monkeypatch.setattr("grit_guardian.analytics.analytics.datetime", MockDatetime)
    monkeypatch.setattr(
        "grit_guardian.persistence.database_manager.datetime", MockDatetime
    )

    return MockDatetime.set_now


# Monkey patching the default database path with mock path
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
    )  # Replace _get_default_db_path instance method

    import grit_guardian.cli

    # Reset tracker to ensure clean state
    grit_guardian.cli._tracker = None

    return CliRunner()


@pytest.fixture
def temp_db():
    """Creates a temporary database file for testing.

    Yields:
        Path object pointing to temporary database file
    """
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp:
        db_path = Path(tmp.name)
        db = DatabaseManager(db_path)
        yield db

        # Cleanup after test
        if db_path.exists():
            db_path.unlink()
        backup_path = db_path.with_suffix(".db.backup")
        if backup_path.exists():
            backup_path.unlink()


@pytest.fixture
def mock_db_with_errors():
    """Creates a mock DatabaseManager that simulates various database errors.

    Returns:
        Mock DatabaseManager instance configured to raise database errors
    """
    import sqlite3

    mock = Mock(spec=DatabaseManager)

    # Configure different error scenarios
    mock.connection_error = sqlite3.DatabaseError("Unable to connect to database")
    mock.integrity_error = sqlite3.IntegrityError("UNIQUE constraint failed")
    mock.operational_error = sqlite3.OperationalError("database is locked")
    mock.corrupt_error = sqlite3.DatabaseError("database disk image is malformed")

    # Method to configure error for specific operation
    def configure_error(operation, error_type):
        if operation == "create_habit":
            mock.create_habit.side_effect = error_type
        elif operation == "add_completion":
            mock.add_completion.side_effect = error_type
        elif operation == "delete_habit":
            mock.delete_habit.side_effect = error_type
        elif operation == "get_habits":
            mock.get_habits.side_effect = error_type
        elif operation == "get_habit_by_name":
            mock.get_habit_by_name.side_effect = error_type
        elif operation == "get_completions":
            mock.get_completions.side_effect = error_type

    mock.configure_error = configure_error
    return mock
