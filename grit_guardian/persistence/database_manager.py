import sqlite3
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Any
from contextlib import contextmanager


# Date and time datatypes in SQLite are stored as TEXT ("YYYY-MM-DD HH:MM:SS.SSS")
# See: https://www.sqlite.org/datatype3.html
def adapt_datetime(dt):
    """Convert datetime to ISO format string for SQLite."""
    return dt.isoformat()


def convert_datetime(s):
    """Convert ISO format string from SQLite to datetime."""
    return datetime.fromisoformat(s.decode())


# For proper date and time handling we register adapter and converter callables.
# See: https://docs.python.org/3/library/sqlite3.html#how-to-convert-sqlite-values-to-custom-python-types
sqlite3.register_adapter(datetime, adapt_datetime)
sqlite3.register_converter("TIMESTAMP", convert_datetime)


class DatabaseManager:
    def __init__(self, db_path: Optional[Path] = None):
        """Initializes the database manager.

        Args:
            db_path: Optional custom database path. If None, uses default XDG config location.
        """
        self.db_path = db_path or self._get_default_db_path()
        self._ensure_config_dir()
        self._init_database()

    def _get_default_db_path(self) -> Path:
        """Gets the default database path following XDG Base Directory specification."""
        config_dir = Path.home() / ".config" / "grit-guardian"
        return config_dir / "habits.db"

    def _ensure_config_dir(self):
        """Ensures the configuration directory exists."""
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

    def _init_database(self):
        """Initialize the database schema."""
        with self._get_connection() as conn:
            # Enable foreign key constraints
            conn.execute("PRAGMA foreign_keys = ON")

            # Create habits table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS habits(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    task TEXT NOT NULL,
                    periodicity TEXT CHECK(periodicity IN ('daily', 'weekly')) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)

            conn.execute("""
                CREATE TABLE IF NOT EXISTS completions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    habit_id INTEGER NOT NULL,
                    completed_at TIMESTAMP NOT NULL,
                    FOREIGN KEY (habit_id) REFERENCES habits(id) ON DELETE CASCADE
                    );
            """)

            # Create index for faster queries
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_completions_habit_id
                ON completions(habit_id)
            """)

            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_completions_completed_at
                ON completions(completed_at)
            """)

    # AI-generated code: Check for validity
    @contextmanager
    def _get_connection(self):
        """Context manager for database connection."""
        conn = None
        try:
            conn = sqlite3.connect(self.db_path, detect_types=sqlite3.PARSE_DECLTYPES)
            conn.row_factory = sqlite3.Row
            # Enable foreign key constraints for this connection
            conn.execute("PRAGMA foreign_keys = ON")
            yield conn
            conn.commit()
        except sqlite3.DatabaseError as e:
            if conn:
                conn.rollback()
            # Attempt to restore from backup if database is corrupted
            if "database disk image is malformed" in str(
                e
            ) or "file is not a database" in str(e):
                self._restore_from_backup()
                raise Exception(
                    "Database was corrupted. Restored from backup. Please retry operation."
                )
            raise
        finally:
            if conn:
                conn.close()

    def create_habit(self, name: str, task: str, periodicity: str) -> int:
        """Creates a new habit.

        Args:
            name: Unique name for the habit
            task: Description of the task
            periodicity: Either 'daily' or 'weekly'

        Returns:
            The ID of the created habit

        Raises:
            sqlite3 Error XXXXXXXXXXX: if habit with same name already exists
            ValueError: If periodicity is invalid
        """
        pass

    def get_habits(self) -> List[Dict[str, Any]]:
        """Gets all habits with their completion counts.

        Returns:
            List of habit dictionaries with completion information
        """
        pass

    def get_habit_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """Gets a specific habit by name.

        Args:
            name: The habit name

        Returns:
            Habit dictionary or None if not found
        """
        pass

    def delete_habit(self, name: str) -> bool:
        """Deletes a habit and all its completions.

        Args:
            name: The habit name to delete

        Returns:
            True if deleted, False if not found
        """
        pass

    def add_completion(
        self, habit_name: str, completed_at: Optional[datetime] = None
    ) -> int:
        """Adds a completion record for a habit.

        Args:
            habit_name: Name of the habit to complete
            completed_at: Optional completion timestamp (defaults to now)

        Raises:
            ValueError: If habit not found
        """
        pass

    def get_completions(
        self, habit_name: str, limit: Optional[int] = None
    ) -> List[datetime]:
        """Gets completion timestamps for a habit.

        Args:
            habit_name: Name of the habit
            limit: Optional limit on number of completions to return

        Returns:
            List of completion timestamps, most recent first
        """
        pass

    def backup_database(self) -> Path:
        """Creates a backup of the database.

        Returns:
            Path to the backup file
        """
        pass

    def _restore_from_backup(self):
        """Restores database from backup if it exists."""
        pass

    def get_stats(self) -> Dict[str, Any]:
        """Gets overall statistics about habits and completions.

        Returns:
            Dictionary with statistics
        """
        pass
