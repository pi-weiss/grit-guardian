import pytest
import sqlite3
import tempfile
from pathlib import Path
from datetime import datetime, timedelta
from grit_guardian.persistence.database_manager import DatabaseManager


@pytest.fixture
def temp_db():
    """Create a temporary database for testing."""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        db_path = Path(f.name)

    db = DatabaseManager(db_path)
    yield db

    # Mr DB Proper cleans the window sesh!
    if db_path.exists():
        db_path.unlink()
    backup_path = db_path.with_suffix(".db.backup")
    if backup_path.exists():
        backup_path.unlink()


class TestDatabaseManager:
    def test_database_creation(self, temp_db):
        """Test that database and tables are created correctly."""
        assert temp_db.db_path.exists()

        with sqlite3.connect(temp_db.db_path) as conn:
            tables = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table';"
            ).fetchall()
            table_names = [t[0] for t in tables]

            assert "habits" in table_names
            assert "completions" in table_names
