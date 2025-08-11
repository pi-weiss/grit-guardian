User Guide
==========

This guide covers all features of Grit Guardian.

Core Concepts
-------------

Habits
~~~~~~

Habits are the building blocks of Grit Guardian. Each habit has:

- **Name**: A unique identifier (e.g., "Morning Reading")
- **Task**: Description of what to do (e.g., "Read for 15 minutes")
- **Periodicity**: How often to do it (``daily`` or ``weekly``)
- **Completions**: Timestamps of when you completed the habit

Periodicity Types
~~~~~~~~~~~~~~~~~

**Daily Habits**
  Should be completed every day. Examples: exercise, reading, meditation.

**Weekly Habits**
  Should be completed once per week. Examples: weekly planning, deep cleaning, grocery shopping.

Your Guardian Companion
~~~~~~~~~~~~~~~~~~~~~~~

Your virtual companion has five mood states based on your habit performance:

- **Ecstatic** 😁: 90%+ completion rate with all active streaks
- **Happy** 😊: 70%+ completion rate
- **Content** 😐: 50%+ completion rate
- **Sad** 😔: 30%+ completion rate
- **Worried** 😟: Below 30% completion rate

Habit Management
----------------

Adding Habits
~~~~~~~~~~~~~

Create new habits with the ``add`` command:

.. code-block:: bash

   gg add "Exercise" "30 minutes of physical activity" daily
   gg add "Weekly Review" "Plan and review the week" weekly

**Best Practices**:
- Use clear, specific names
- Write actionable task descriptions
- Start with achievable goals

Listing Habits
~~~~~~~~~~~~~~

View all your habits:

.. code-block:: bash

   gg list

Output shows name, task description, and periodicity for each habit.

Deleting Habits
~~~~~~~~~~~~~~~

Remove habits you no longer want to track:

.. code-block:: bash

   gg delete "Old Habit"

You'll be prompted for confirmation. This permanently removes the habit and all its completion history.

Tracking Completions
--------------------

Completing Habits
~~~~~~~~~~~~~~~~~

Mark habits as complete when you finish them:

.. code-block:: bash

   gg complete "Morning Reading"

**Important Notes**:
- Daily habits can only be completed once per day
- Weekly habits can only be completed once per week (Monday-Sunday)
- Completions are timestamped for accurate tracking

Viewing Status
~~~~~~~~~~~~~~

Check what's pending and completed for today:

.. code-block:: bash

   gg status

The output shows:
- **Pending**: Habits not yet completed today/this week
- **Completed**: Habits finished today/this week
- **Progress**: Completion ratio (e.g., "2/5")

Analytics & Progress
--------------------

Streak Analytics
~~~~~~~~~~~~~~~~

View detailed streak information:

.. code-block:: bash

   gg streaks

For each habit, you'll see:
- **Current Streak**: Consecutive completions ending today
- **Longest Streak**: Best streak ever achieved
- **Completion Rate**: Percentage of expected completions since creation

Weekly Progress
~~~~~~~~~~~~~~~

See a visual weekly calendar:

.. code-block:: bash

   gg weekly

Shows an ASCII table with:
- ✓ = Completed
- ✗ = Missed  
- \- = Future/Not applicable

Identifying Struggles
~~~~~~~~~~~~~~~~~~~~~

Find habits needing attention:

.. code-block:: bash

   gg struggled
   gg struggled --since 14  # Check last 14 days

Shows habits with completion rates below 50% in the specified period.

Pet Interaction
---------------

Checking Your Companion
~~~~~~~~~~~~~~~~~~~~~~~

View your Guardian:

.. code-block:: bash

   gg pet

The display shows:
- ASCII art reflecting current mood
- Pet's name and mood state
- Mood-specific message
- Tips based on performance

Understanding Pet Moods
~~~~~~~~~~~~~~~~~~~~~~~~

Your pet's mood updates based on:
- **Average completion rate** across all habits
- **Active streaks** (habits completed recently)
- **Overall consistency** in your tracking

Tips for a Happy Pet:
- Maintain streaks on multiple habits
- Keep completion rates above 70%
- Don't abandon habits for too long

Advanced Features
-----------------

Data Storage
~~~~~~~~~~~~

Habit data is stored locally in:
- **Linux/macOS**: ``~/.config/grit-guardian/habits.db``
- **Windows**: ``%APPDATA%\\grit-guardian\\habits.db``

The database is a standard SQLite file that you can:
- Back up by copying the file
- Examine with SQLite tools
- Reset by deleting the file (then run ``gg init``)

Sample Data
~~~~~~~~~~~

The ``init`` command creates sample habits:

.. code-block:: bash

   gg init

This only works on empty databases. If you already have habits, it shows your current status instead.

Database Reset
~~~~~~~~~~~~~~

To start fresh (⚠️ **destroys all data**):

.. code-block:: bash

   rm ~/.config/grit-guardian/habits.db  # Linux/macOS
   # or del %APPDATA%\\grit-guardian\\habits.db  # Windows
   gg init

Tips & Best Practices
---------------------

Habit Design
~~~~~~~~~~~~

1. **Start Small**: Begin with 2-3 habits you can easily maintain
2. **Be Specific**: "Read" → "Read for 15 minutes"
3. **Make it Achievable**: Set realistic expectations
4. **Stack Habits**: Link new habits to existing routines

Tracking Strategy
~~~~~~~~~~~~~~~~~

1. **Daily Check-ins**: Use ``gg status`` every morning or evening
2. **Weekly Reviews**: Run ``gg weekly`` to spot patterns
3. **Address Struggles**: Use ``gg struggled`` to identify problems early
4. **Celebrate Success**: Check ``gg pet`` when you're doing well

Long-term Success
~~~~~~~~~~~~~~~~~

1. **Consistency over Perfection**: Don't abandon habits after missing a day
2. **Adjust as Needed**: Delete or modify habits that aren't working
3. **Use Your Pet**: Let the mood feedback guide your priorities
4. **Review Regularly**: Weekly planning helps maintain focus

Common Workflows
----------------

Daily Routine
~~~~~~~~~~~~~

.. code-block:: bash

   # Morning: Check what's due
   gg status

   # Throughout day: Complete habits
   gg complete "Morning Reading"
   gg complete "Exercise"

   # Evening: Review progress
   gg status
   gg pet

Weekly Review
~~~~~~~~~~~~~

.. code-block:: bash

   # See weekly patterns
   gg weekly

   # Identify problems
   gg struggled

   # Complete weekly habits
   gg complete "Weekly Planning"

   # Check overall progress
   gg streaks

Monthly Maintenance
~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Review all habits
   gg list

   # Check long-term trends
   gg struggled --since 30

   # Consider adding/removing habits
   gg add "New Habit" "Description" daily
   gg delete "Old Habit"

Troubleshooting
---------------

Common Issues
~~~~~~~~~~~~~

**"Habit already completed today"**
  You can only complete daily habits once per day. Weekly habits once per week.

**Pet always worried**
  Your completion rates may be low. Use ``gg struggled`` to identify problems.

**Can't find habit**
  Check exact spelling with ``gg list``. Habit names are case-sensitive.

**Database errors**
  Try deleting and recreating: ``rm ~/.config/grit-guardian/habits.db && gg init``

Performance Tips
~~~~~~~~~~~~~~~~

- The CLI is designed to be fast for daily use
- All data is stored locally (no internet required)
- Database operations are optimized for small datasets
- Commands typically complete in under 100ms

Getting Help
------------

- Use ``--help`` with any command: ``gg add --help``
- Check command-specific documentation in :doc:`cli_reference`
- Report bugs on `GitHub Issues <https://github.com/pi-weiss/grit-guardian/issues>`_
