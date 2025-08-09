Contributing Guide
=================

Thank you for your interest in contributing to Grit Guardian! This guide will help you get started.

Getting Started
---------------

Prerequisites
~~~~~~~~~~~~~

- Python 3.9 or higher
- Poetry for dependency management
- Git for version control

Development Setup
~~~~~~~~~~~~~~~~~

1. **Fork and clone the repository**:

   .. code-block:: bash

      git clone https://github.com/yourusername/grit-guardian.git
      cd grit-guardian

2. **Install Poetry** (if not already installed):

   .. code-block:: bash

      curl -sSL https://install.python-poetry.org | python3 -

3. **Install dependencies**:

   .. code-block:: bash

      poetry install

4. **Activate the virtual environment**:

   .. code-block:: bash

      poetry shell

5. **Verify the setup**:

   .. code-block:: bash

      poetry run pytest
      poetry run gg --help

Development Workflow
--------------------

Making Changes
~~~~~~~~~~~~~~

1. **Create a feature branch**:

   .. code-block:: bash

      git checkout -b feature/your-feature-name

2. **Make your changes** following our coding standards

3. **Write tests** for new functionality

4. **Run the test suite**:

   .. code-block:: bash

      poetry run pytest

5. **Run code quality checks**:

   .. code-block:: bash

      poetry run black grit_guardian tests
      poetry run isort grit_guardian tests  
      poetry run flake8 grit_guardian tests
      poetry run mypy grit_guardian

6. **Commit your changes**:

   .. code-block:: bash

      git add .
      git commit -m "feat: add your feature description"

7. **Push and create a pull request**:

   .. code-block:: bash

      git push origin feature/your-feature-name

Coding Standards
----------------

Code Style
~~~~~~~~~~

We use these tools to maintain consistent code style:

- **Black** for code formatting
- **isort** for import sorting  
- **flake8** for linting
- **mypy** for type checking

Run all checks with:

.. code-block:: bash

   poetry run black grit_guardian tests
   poetry run isort grit_guardian tests
   poetry run flake8 grit_guardian tests
   poetry run mypy grit_guardian

Type Hints
~~~~~~~~~~

- Use type hints for all function parameters and return values
- Import types from ``typing`` module when needed
- Use ``Optional[T]`` for nullable parameters

Example:

.. code-block:: python

   from typing import List, Optional
   from datetime import datetime

   def create_habit(name: str, task: str, periodicity: str) -> Optional[Habit]:
       """Create a new habit with validation."""
       # Implementation here
       pass

Documentation
~~~~~~~~~~~~~

- Write docstrings for all public functions and classes
- Use Google-style docstrings
- Include parameter types, return types, and examples

Example:

.. code-block:: python

   def calculate_streak(completions: List[datetime], periodicity: str) -> int:
       """Calculate the current streak for a habit.
       
       Args:
           completions: List of completion timestamps
           periodicity: Either 'daily' or 'weekly'
           
       Returns:
           Number of consecutive completions ending today
           
       Examples:
           >>> from datetime import datetime
           >>> completions = [datetime.now(), datetime.now() - timedelta(days=1)]
           >>> calculate_streak(completions, 'daily')
           2
       """

Testing
-------

Test Structure
~~~~~~~~~~~~~~

Tests are organized in the ``tests/`` directory:

.. code-block:: text

   tests/
   ├── conftest.py              # Shared fixtures
   ├── test_cli.py             # CLI command tests
   ├── test_habit_tracker.py   # Business logic tests
   ├── test_database_manager.py # Database tests
   ├── test_analytics.py       # Analytics tests
   ├── test_models.py          # Model tests
   ├── test_pet.py             # Pet system tests
   └── integration/
       └── test_full_workflow.py # Integration tests

Writing Tests
~~~~~~~~~~~~~

1. **Unit tests** for individual functions/methods
2. **Integration tests** for complete workflows
3. **CLI tests** using Click's testing utilities
4. **Property-based tests** for mathematical functions

Example unit test:

.. code-block:: python

   def test_add_habit_success(self, habit_tracker):
       """Test successfully adding a new habit."""
       habit = habit_tracker.add_habit("Exercise", "Daily workout", "daily")
       
       assert habit.name == "Exercise"
       assert habit.task == "Daily workout"
       assert habit.periodicity == Periodicity.DAILY

Test Coverage
~~~~~~~~~~~~~

We maintain 90%+ test coverage. Check coverage with:

.. code-block:: bash

   poetry run pytest --cov=grit_guardian --cov-report=html
   open htmlcov/index.html

Commit Message Format
---------------------

We use Conventional Commits format:

.. code-block:: text

   <type>[optional scope]: <description>

   [optional body]

   [optional footer(s)]

Types:
- ``feat``: New feature
- ``fix``: Bug fix  
- ``docs``: Documentation changes
- ``style``: Code style changes (formatting, etc.)
- ``refactor``: Code refactoring
- ``test``: Adding or updating tests
- ``chore``: Maintenance tasks

Examples:

.. code-block:: bash

   git commit -m "feat: add weekly habit support"
   git commit -m "fix: handle database connection errors"
   git commit -m "docs: update installation guide"

Pull Request Process
--------------------

1. **Ensure all tests pass** and coverage is maintained
2. **Update documentation** if you've changed APIs or added features
3. **Write a clear PR description** explaining what and why
4. **Link to relevant issues** if applicable
5. **Respond to review feedback** promptly

PR Template:

.. code-block:: markdown

   ## Description
   Brief description of changes

   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature  
   - [ ] Documentation update
   - [ ] Refactoring

   ## Testing
   - [ ] Tests pass locally
   - [ ] Added tests for new functionality
   - [ ] Updated documentation

   ## Checklist
   - [ ] Code follows style guidelines
   - [ ] Self-review completed
   - [ ] Documentation updated

Issue Reporting
---------------

When reporting bugs or requesting features:

Bug Reports
~~~~~~~~~~~

Include:
- **Steps to reproduce** the issue
- **Expected behavior** vs actual behavior
- **Environment details** (OS, Python version, etc.)
- **Error messages** or stack traces
- **Minimal example** if possible

Feature Requests
~~~~~~~~~~~~~~~~

Include:
- **Clear description** of the feature
- **Use case** or motivation
- **Proposed implementation** (if you have ideas)
- **Alternatives considered**

Areas for Contribution
----------------------

We welcome contributions in these areas:

High Priority
~~~~~~~~~~~~~

- **Bug fixes** and error handling improvements  
- **Performance optimizations**
- **Test coverage** improvements
- **Documentation** enhancements

Medium Priority
~~~~~~~~~~~~~~~

- **New analytics features** (charts, exports, etc.)
- **Pet system enhancements** (new moods, animations)
- **CLI improvements** (better formatting, colors)
- **Database features** (backup, import/export)

Low Priority
~~~~~~~~~~~~

- **Web interface** (optional dashboard)
- **Mobile companion app**
- **Habit templates** and categories
- **Notification system**

Development Environment
-----------------------

Recommended Tools
~~~~~~~~~~~~~~~~~

- **IDE**: PyCharm, VS Code, or similar with Python support
- **Terminal**: iTerm2 (macOS), Windows Terminal (Windows), or your preferred terminal
- **Git GUI**: GitKraken, Sourcetree, or command-line git

Useful Commands
~~~~~~~~~~~~~~~

.. code-block:: bash

   # Run tests in watch mode
   poetry run pytest-watch

   # Run specific test
   poetry run pytest tests/test_cli.py::TestCLIAdd::test_add_habit_success

   # Run linting only
   poetry run flake8 grit_guardian

   # Format code
   poetry run black grit_guardian tests

   # Start development server (if building web features)
   poetry run python -m grit_guardian.server

Debugging
~~~~~~~~~

- Use ``pytest -s`` to see print statements during tests
- Use ``pdb`` or ``ipdb`` for interactive debugging
- Check logs in ``~/.config/grit-guardian/`` for runtime issues

Community Guidelines
--------------------

Code of Conduct
~~~~~~~~~~~~~~~

- **Be respectful** and inclusive in all interactions
- **Provide constructive feedback** in code reviews
- **Help newcomers** get started with the project
- **Focus on technical merit** in discussions

Communication
~~~~~~~~~~~~~

- **GitHub Issues** for bug reports and feature requests
- **GitHub Discussions** for general questions and ideas
- **Pull Request comments** for code-specific discussions

Recognition
~~~~~~~~~~~

Contributors are recognized:
- In the project's ``CONTRIBUTORS.md`` file
- In release notes for significant contributions
- With GitHub's contributor recognition features

Getting Help
------------

If you need help:

1. **Check existing documentation** and issues
2. **Ask in GitHub Discussions** for general questions
3. **Create an issue** for specific bugs or feature requests
4. **Tag maintainers** if you need urgent help

Thank you for contributing to Grit Guardian! 🐉
