import pytest
import tempfile
from pathlib import Path

from grit_guardian.persistence.database_manager import DatabaseManager


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
        yield db_path
        # Cleanup after test
        if db_path.exists():
            db_path.unlink()
        backup_path = db_path.with_suffix(".db.backup")
        if backup_path.exists():
            backup_path.unlink()
