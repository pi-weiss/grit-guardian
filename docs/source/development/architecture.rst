Architecture Guide
==================

This document describes the architecture and design principles of Grit Guardian.

Overview
--------

Grit Guardian follows a layered architecture with clear separation of concerns:

.. code-block:: text

   ┌─────────────────────────────────────────┐
   │              CLI Layer                  │  ← User Interface
   │         (grit_guardian.cli)             │
   └─────────────────┬───────────────────────┘
                     │
   ┌─────────────────▼───────────────────────┐
   │            Service Layer                │  ← Business Logic
   │    (grit_guardian.core.habit_tracker)   │
   └─────┬───────────────────────────┬───────┘
         │                           │
   ┌─────▼──────┐              ┌─────▼──────┐
   │  Analytics │              │    Pet     │  ← Domain Services
   │   Module   │              │   System   │
   └────────────┘              └────────────┘
         │                           │
   ┌─────▼───────────────────────────▼───────┐
   │            Data Layer                   │  ← Persistence
   │  (grit_guardian.persistence.database)   │
   └─────────────────────────────────────────┘

Design Principles
-----------------

Single Responsibility
~~~~~~~~~~~~~~~~~~~~~

Each module has a single, well-defined responsibility:

- **CLI**: User interface and command parsing
- **HabitTracker**: Business logic orchestration
- **DatabaseManager**: Data persistence operations
- **Analytics**: Calculations and statistics
- **Pet**: Virtual companion system
- **Models**: Data structures and validation

Dependency Injection
~~~~~~~~~~~~~~~~~~~~

Components receive their dependencies rather than creating them:

.. code-block:: python

   # HabitTracker receives DatabaseManager
   class HabitTracker:
       def __init__(self, db_manager: DatabaseManager):
           self.db = db_manager

   # CLI creates and injects dependencies
   db_manager = DatabaseManager()
   tracker = HabitTracker(db_manager)

Functional Programming
~~~~~~~~~~~~~~~~~~~~~~

Analytics module uses functional programming principles:

.. code-block:: python

   # Pure functions with no side effects
   def calculate_streak(completions: List[datetime], periodicity: str) -> int:
       """Calculate streak based on input data only."""
       # Implementation uses only input parameters

   # Immutable data structures where possible
   @dataclass(frozen=True)
   class AnalyticsResult:
       current_streak: int
       longest_streak: int
       completion_rate: float

Module Architecture
-------------------

CLI Layer
~~~~~~~~~

**Location**: ``grit_guardian.cli``

**Responsibilities**:
- Command-line argument parsing
- User input validation  
- Output formatting and display
- Error message presentation

**Key Components**:

.. code-block:: python

   @click.group()
   def main():
       """Main CLI entry point."""
       
   @main.command()
   def add(name: str, task: str, periodicity: str):
       """Add habit command implementation."""

**Design Patterns**:
- **Command Pattern**: Each CLI command maps to a specific action
- **Facade Pattern**: CLI provides simple interface to complex business logic

Service Layer
~~~~~~~~~~~~~

**Location**: ``grit_guardian.core.habit_tracker``

**Responsibilities**:
- Business rule enforcement
- Transaction coordination
- Data validation
- Error handling and conversion

**Key Components**:

.. code-block:: python

   class HabitTracker:
       def add_habit(self, name: str, task: str, periodicity: str) -> Habit:
           """Add new habit with validation."""
           
       def complete_habit(self, name: str) -> bool:
           """Complete habit with business rules."""

**Design Patterns**:
- **Service Layer Pattern**: Encapsulates business logic
- **Repository Pattern**: Abstracts data access through DatabaseManager

Data Models
~~~~~~~~~~~

**Location**: ``grit_guardian.core.models``

**Responsibilities**:
- Data structure definitions
- Basic validation logic
- Type safety and serialization

**Key Components**:

.. code-block:: python

   @dataclass
   class Habit:
       id: Optional[int]
       name: str
       task: str
       periodicity: Periodicity
       created_at: datetime
       completions: List[datetime]

**Design Patterns**:
- **Data Transfer Object (DTO)**: Habit carries data between layers
- **Value Object**: Periodicity enum represents domain concepts

Persistence Layer
~~~~~~~~~~~~~~~~~

**Location**: ``grit_guardian.persistence.database_manager``

**Responsibilities**:
- Database connection management
- SQL query execution
- Data mapping and conversion
- Transaction handling

**Key Components**:

.. code-block:: python

   class DatabaseManager:
       def create_habit(self, name: str, task: str, periodicity: str) -> int:
           """Create habit in database."""
           
       def get_habits(self) -> List[Dict[str, Any]]:
           """Retrieve all habits with metadata."""

**Design Patterns**:
- **Repository Pattern**: Provides collection-like interface to data
- **Unit of Work**: Manages transactions and consistency

Analytics Module
~~~~~~~~~~~~~~~~

**Location**: ``grit_guardian.analytics.analytics``

**Responsibilities**:
- Streak calculations
- Statistical analysis
- Performance metrics
- Data aggregation

**Key Components**:

.. code-block:: python

   def calculate_streak(completions: List[datetime], periodicity: str) -> int:
       """Pure function for streak calculation."""
       
   def get_habit_analytics(name: str, created_at: datetime, 
                          completions: List[datetime], periodicity: str) -> Dict:
       """Comprehensive habit analysis."""

**Design Patterns**:
- **Strategy Pattern**: Different algorithms for daily vs weekly calculations
- **Pure Functions**: No side effects, easier to test and reason about

Pet System
~~~~~~~~~~

**Location**: ``grit_guardian.pet.pet``

**Responsibilities**:
- Mood calculation based on habits
- ASCII art generation
- Motivational messaging
- Visual feedback system

**Key Components**:

.. code-block:: python

   class Pet:
       def calculate_mood(self, habits_data: List[Dict]) -> PetMood:
           """Calculate mood based on habit performance."""
           
       def get_ascii_art(self) -> str:
           """Generate mood-appropriate ASCII art."""

**Design Patterns**:
- **State Pattern**: Pet mood affects behavior and appearance
- **Template Method**: Mood calculation follows consistent algorithm

Data Flow
---------

Typical Request Flow
~~~~~~~~~~~~~~~~~~~~

1. **CLI Command**: User runs ``gg complete "Exercise"``
2. **Command Parsing**: Click parses arguments and calls complete()
3. **Service Call**: CLI calls ``tracker.complete_habit("Exercise")``
4. **Business Logic**: HabitTracker validates and applies business rules
5. **Data Access**: HabitTracker calls ``db.add_completion()``
6. **Database Update**: DatabaseManager executes SQL INSERT
7. **Response**: Success/failure propagates back through layers
8. **Output**: CLI displays confirmation message

.. code-block:: text

   User Input → CLI → HabitTracker → DatabaseManager → SQLite
                ↓
   Output ← CLI ← HabitTracker ← DatabaseManager ← SQLite

Error Handling Flow
~~~~~~~~~~~~~~~~~~~

Errors are handled at appropriate layers:

.. code-block:: python

   # DatabaseManager: Low-level errors
   try:
       conn.execute(sql, params)
   except sqlite3.Error as e:
       raise DatabaseError(f"SQL error: {e}")

   # HabitTracker: Business logic errors  
   if not habit:
       raise HabitNotFoundError(f"Habit '{name}' not found")

   # CLI: User-friendly error display
   try:
       tracker.complete_habit(name)
       click.echo("✓ Completed!")
   except HabitNotFoundError as e:
       click.echo(f"✗ {e}", err=True)

Database Design
---------------

Schema Overview
~~~~~~~~~~~~~~~

.. code-block:: sql

   -- Core habit definition
   CREATE TABLE habits (
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       name TEXT UNIQUE NOT NULL,
       task TEXT NOT NULL,
       periodicity TEXT CHECK(periodicity IN ('daily', 'weekly')),
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
   );

   -- Completion tracking
   CREATE TABLE completions (
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       habit_id INTEGER NOT NULL,
       completed_at TIMESTAMP NOT NULL,
       FOREIGN KEY (habit_id) REFERENCES habits(id) ON DELETE CASCADE
   );

Design Decisions
~~~~~~~~~~~~~~~~

**Normalized Structure**: Separate tables for habits and completions allow:
- Efficient queries for completion history
- Referential integrity with foreign keys
- Easy addition of completion metadata

**Timestamp Storage**: All times stored as ISO format strings:
- Timezone-agnostic
- Easy parsing and formatting
- Compatible across platforms

**Referential Integrity**: Foreign key constraints ensure:
- Orphaned completions are automatically deleted
- Data consistency is maintained
- Database-level validation

Configuration Management
------------------------

Configuration Sources
~~~~~~~~~~~~~~~~~~~~~

Configuration is loaded from multiple sources in order of precedence:

1. **Command-line arguments** (highest priority)
2. **Environment variables**
3. **Configuration files**
4. **Default values** (lowest priority)

.. code-block:: python

   # Environment variables
   XDG_CONFIG_HOME  # Base config directory
   GG_DATABASE_PATH # Custom database location

File Locations
~~~~~~~~~~~~~~

Following XDG Base Directory Specification:

- **Linux/macOS**: ``~/.config/grit-guardian/``
- **Windows**: ``%APPDATA%\grit-guardian\``

Files:
- ``habits.db`` - SQLite database
- ``config.json`` - User preferences (future)
- ``backups/`` - Automatic backups (future)

Testing Architecture
--------------------

Test Pyramid
~~~~~~~~~~~~

.. code-block:: text

                    ┌──────────────────┐
                    │   Integration    │  ← Few, complex
                    │      Tests       │
                    └──────────────────┘
                  ┌────────────────────────┐
                  │     Service Tests      │  ← More, focused
                  └────────────────────────┘
                ┌──────────────────────────────┐
                │        Unit Tests            │  ← Many, fast
                └──────────────────────────────┘

Test Isolation
~~~~~~~~~~~~~~

Each test layer is isolated:

.. code-block:: python

   # Unit tests: Mock all dependencies
   def test_calculate_streak(self):
       completions = [datetime.now()]
       result = calculate_streak(completions, 'daily')
       assert result == 1

   # Service tests: Use test database
   def test_add_habit(self, temp_db):
       db = DatabaseManager(temp_db)
       tracker = HabitTracker(db)
       habit = tracker.add_habit("Test", "Task", "daily")
       assert habit.name == "Test"

   # Integration tests: Full system
   def test_cli_workflow(self, isolated_cli_runner):
       result = runner.invoke(main, ['add', 'Test', 'Task', 'daily'])
       assert result.exit_code == 0

Performance Considerations
--------------------------

Database Optimization
~~~~~~~~~~~~~~~~~~~~~

- **Indexes**: On frequently queried columns (habit_id, completed_at)
- **Query Efficiency**: Minimize N+1 queries with JOINs
- **Connection Management**: Single connection per operation
- **Transaction Batching**: Group related operations

Memory Management
~~~~~~~~~~~~~~~~~

- **Lazy Loading**: Load completions only when needed
- **Data Structures**: Use appropriate collections (lists vs sets)
- **Caching**: Cache frequently accessed data in memory
- **Cleanup**: Explicit resource cleanup where needed

Scalability Limits
~~~~~~~~~~~~~~~~~~~

Current architecture is optimized for:
- **Habits**: Up to 1,000 active habits
- **Completions**: Up to 100,000 completion records
- **Response Time**: < 100ms for typical operations
- **Database Size**: Up to 100MB

Future scaling may require:
- Database connection pooling
- Background processing for analytics
- Data archiving strategies

Security Considerations
-----------------------

Data Protection
~~~~~~~~~~~~~~~

- **Local Storage**: All data stored locally, no cloud dependencies
- **File Permissions**: Database files have appropriate permissions
- **Input Validation**: All user input is validated and sanitized
- **SQL Injection**: Parameterized queries prevent injection attacks

Privacy
~~~~~~~

- **No Tracking**: No analytics or usage tracking
- **No Network**: No network connections required
- **User Control**: Users have full control over their data
- **Data Portability**: Standard SQLite format allows easy migration

Extensibility
-------------

Plugin Architecture (Future)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Potential extension points:

.. code-block:: python

   # Custom analytics plugins
   class AnalyticsPlugin:
       def calculate_custom_metric(self, habits: List[Habit]) -> Dict:
           pass

   # Custom pet behaviors
   class PetPlugin:
       def get_custom_ascii_art(self, mood: PetMood) -> str:
           pass

   # Export/import plugins
   class DataPlugin:
       def export_data(self, habits: List[Habit]) -> bytes:
           pass

API Stability
~~~~~~~~~~~~~

Public APIs are designed for stability:

- **Semantic Versioning**: Major.Minor.Patch versioning
- **Deprecation Policy**: 2-version deprecation cycle
- **Backward Compatibility**: Maintain compatibility within major versions

Deployment
----------

Distribution Strategy
~~~~~~~~~~~~~~~~~~~~~

- **PyPI Package**: Primary distribution method
- **GitHub Releases**: Source code and binaries
- **Docker Images**: Containerized deployment (future)
- **Package Managers**: OS-specific packages (future)

Installation Methods
~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # PyPI (recommended)
   pip install grit-guardian

   # Development install
   git clone repo && pip install -e .

   # Poetry (for contributors)
   git clone repo && poetry install

Monitoring and Observability
----------------------------

Logging Strategy
~~~~~~~~~~~~~~~~

.. code-block:: python

   # Structured logging
   import logging

   logger = logging.getLogger(__name__)

   def add_habit(self, name: str, task: str, periodicity: str) -> Habit:
       logger.info("Adding habit", extra={
           "habit_name": name,
           "periodicity": periodicity
       })

Error Tracking
~~~~~~~~~~~~~~

- **Exception Handling**: Comprehensive error handling at all layers
- **Error Classification**: Different error types for different scenarios
- **User Feedback**: Clear, actionable error messages
- **Debug Information**: Detailed logging for troubleshooting

This architecture provides a solid foundation for Grit Guardian while maintaining flexibility for future enhancements.
