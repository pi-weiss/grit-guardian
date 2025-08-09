CLI Reference
=============

This page documents all available commands and their options.

Main Command
------------

.. code-block:: bash

   grit-guardian [OPTIONS] COMMAND [ARGS]...
   # or
   gg [OPTIONS] COMMAND [ARGS]...

**Description**: Grit Guardian - Terminal-based habit tracker with virtual pet

**Global Options**:

--help
  Show help message and exit

Commands Overview
-----------------

Habit Management
~~~~~~~~~~~~~~~~

- :ref:`add <cmd-add>` - Add a new habit
- :ref:`list <cmd-list>` - List all habits  
- :ref:`delete <cmd-delete>` - Delete a habit

Progress Tracking
~~~~~~~~~~~~~~~~~

- :ref:`complete <cmd-complete>` - Mark a habit as completed
- :ref:`status <cmd-status>` - Show today's habit status
- :ref:`streaks <cmd-streaks>` - View streak analytics

Analytics & Insights
~~~~~~~~~~~~~~~~~~~~~

- :ref:`weekly <cmd-weekly>` - Show weekly progress view
- :ref:`struggled <cmd-struggled>` - Show habits needing attention
- :ref:`pet <cmd-pet>` - View your Guardian pet

Setup
~~~~~

- :ref:`init <cmd-init>` - Initialize with sample habits

Detailed Command Reference
--------------------------

.. _cmd-add:

add
~~~

Add a new habit to track.

**Syntax**:

.. code-block:: bash

   gg add NAME TASK PERIODICITY

**Arguments**:

NAME
  Unique name for the habit (must be quoted if contains spaces)

TASK  
  Description of what the habit involves

PERIODICITY
  How often to do the habit (``daily`` or ``weekly``)

**Examples**:

.. code-block:: bash

   gg add Exercise "30 minutes of physical activity" daily
   gg add "Weekly Review" "Plan and review the upcoming week" weekly
   gg add Meditation "10 minutes of mindfulness practice" daily

**Error Cases**:
- Duplicate habit names
- Invalid periodicity (not "daily" or "weekly")
- Empty name or task

.. _cmd-list:

list
~~~~

Display all your habits with their details.

**Syntax**:

.. code-block:: bash

   gg list

**Output Format**:
- Bullet-pointed list
- Shows: name - task (periodicity)
- Sorted by creation order

**Example Output**:

.. code-block:: text

   Your Habits:
   --------------------------------------------------
   • Morning Reading - Read for 15 minutes (daily)
   • Exercise - Physical activity (daily)
   • Weekly Planning - Review week (weekly)

.. _cmd-delete:

delete  
~~~~~~

Remove a habit and all its completion history.

**Syntax**:

.. code-block:: bash

   gg delete NAME

**Arguments**:

NAME
  Name of the habit to delete (must match exactly)

**Behavior**:
- Prompts for confirmation
- Permanently removes habit and all completions
- Cannot be undone

**Examples**:

.. code-block:: bash

   gg delete Exercise
   gg delete "Old Habit"

.. _cmd-complete:

complete
~~~~~~~~

Mark a habit as completed for today (daily) or this week (weekly).

**Syntax**:

.. code-block:: bash

   gg complete NAME

**Arguments**:

NAME
  Name of the habit to complete (must match exactly)

**Behavior**:
- Records completion timestamp
- Daily habits: once per calendar day
- Weekly habits: once per calendar week (Monday-Sunday)
- Prevents duplicate completions

**Examples**:

.. code-block:: bash

   gg complete "Morning Reading"
   gg complete Exercise

**Error Cases**:
- Habit not found
- Already completed today/this week

.. _cmd-status:

status
~~~~~~

Show today's habit completion status.

**Syntax**:

.. code-block:: bash

   gg status

**Output Sections**:
- **Pending**: Habits not completed today/this week
- **Completed**: Habits finished today/this week  
- **Progress**: Ratio of completed to total habits

**Example Output**:

.. code-block:: text

   📊 Today's Status
   ==============================

   ⏳ Pending:
     • Morning Reading
     • Exercise

   ✅ Completed:
     • Weekly Planning

   Progress: 1/3
   🎉 All habits completed!

.. _cmd-streaks:

streaks
~~~~~~~

View detailed analytics for all habits.

**Syntax**:

.. code-block:: bash

   gg streaks

**Output Format**:
For each habit:
- Current streak (consecutive completions ending today)
- Longest streak ever achieved
- Completion rate since creation

Plus overall statistics:
- Total active streaks
- Average completion rate

**Example Output**:

.. code-block:: text

   🔥 Habit Streaks & Analytics
   ============================================================

   📌 Morning Reading
      Current Streak: 5 days
      Longest Streak: 12 days  
      Completion Rate: 78.3%

   ------------------------------------------------------------
   📊 Overall Stats:
      Total Active Streaks: 8
      Average Completion Rate: 72.5%

.. _cmd-weekly:

weekly
~~~~~~

Display a weekly progress table showing completion patterns.

**Syntax**:

.. code-block:: bash

   gg weekly

**Output Format**:
- ASCII table with days of the week as columns
- Rows for each habit
- Symbols: ✓ (completed), ✗ (missed), - (future/not applicable)

**Example Output**:

.. code-block:: text

   📅 Weekly Progress
   ============================================================
   Habit                | Mon | Tue | Wed | Thu | Fri | Sat | Sun
   ------------------------------------------------------------
   Morning Reading      |  ✓  |  ✓  |  ✗  |  ✓  |  -  |  -  |  -
   Exercise            |  ✓  |  ✗  |  ✗  |  ✓  |  -  |  -  |  -

   ------------------------------------------------------------
   ✓ = Completed  |  ✗ = Missed  |  - = Future

.. _cmd-struggled:

struggled
~~~~~~~~~

Identify habits with low completion rates that need attention.

**Syntax**:

.. code-block:: bash

   gg struggled [OPTIONS]

**Options**:

--since INTEGER
  Number of days to analyze (default: 30)

**Output Format**:
- Lists habits with <50% completion rate in specified period
- Shows completion rate and number of missed completions
- Sorted by completion rate (worst first)

**Examples**:

.. code-block:: bash

   gg struggled                # Last 30 days
   gg struggled --since 14     # Last 14 days
   gg struggled --since 7      # Last week

**Example Output**:

.. code-block:: text

   ⚠️  Habits needing attention (last 30 days):
   ==================================================

   • Meditation
     Completion rate: 23%
     Missed: 23 times

   💡 Tip: Focus on one habit at a time to build momentum!

.. _cmd-pet:

pet
~~~

View your Guardian dragon and its current mood.

**Syntax**:

.. code-block:: bash

   gg pet

**Output Sections**:
- ASCII art showing pet's appearance
- Pet's current mood state
- Mood-specific message
- Tips based on performance

**Mood States**:
- **Ecstatic**: 90%+ completion, all streaks active
- **Happy**: 70%+ completion rate
- **Content**: 50%+ completion rate
- **Sad**: 30%+ completion rate  
- **Worried**: <30% completion rate

**Example Output**:

.. code-block:: text

   🐉 Your Grit Guardian
   ========================================
       /\   /\
      (  ^.^  )
     <  \___/  >
      \  ~~~  /

   ----------------------------------------
   Name: Guardian
   Mood: Happy

   I'm pleased with your recent progress! Keep up the good work.

   ⭐ Amazing work! Keep up the great consistency!

.. _cmd-init:

init
~~~~

Initialize Grit Guardian with sample habits for new users.

**Syntax**:

.. code-block:: bash

   gg init

**Behavior**:
- Only works if no habits exist
- Creates 4 sample habits:
  - Morning Reading (daily)
  - Exercise (daily)
  - Weekly Planning (weekly)  
  - Learn Something New (daily)
- Shows quick start guide
- Displays initial pet state

**If habits already exist**:
- Shows current habit count
- Displays pet mood
- Suggests using other commands

**Example Output** (new user):

.. code-block:: text

   🐉 Welcome to Grit Guardian!

   ✓ Created sample habits to get you started:
     • Morning Reading - Read for 15 minutes
     • Exercise - Physical activity for 30 minutes
     • Weekly Planning - Review and plan upcoming week
     • Learn Something New - Spend time learning a new skill

   🎯 Quick Start Guide:
     - View your habits: grit-guardian list
     - Complete a habit: grit-guardian complete "Morning Reading"
     - Check your pet: grit-guardian pet
     - See weekly progress: grit-guardian weekly

   Your Guardian dragon is waiting to see your progress!

Exit Codes
----------

All commands use standard exit codes:

- **0**: Success
- **1**: General error (invalid arguments, habit not found, etc.)
- **2**: Command line usage error

Shell Completion
----------------

Grit Guardian supports shell completion for command and habit names. Setup varies by shell:

**Bash**:

.. code-block:: bash

   # Add to ~/.bashrc
   eval "$(_GG_COMPLETE=bash_source gg)"

**Zsh**:

.. code-block:: zsh

   # Add to ~/.zshrc  
   eval "$(_GG_COMPLETE=zsh_source gg)"

**Fish**:

.. code-block:: fish

   # Add to ~/.config/fish/config.fish
   eval (env _GG_COMPLETE=fish_source gg)

Environment Variables
---------------------

**XDG_CONFIG_HOME**
  Base directory for configuration files. Defaults to ``~/.config``.
  Database will be stored at ``$XDG_CONFIG_HOME/grit-guardian/habits.db``.

Output Formats
--------------

All output is designed for terminal display with:
- Emoji for visual appeal
- Colors for status indication  
- Clear formatting and alignment
- Consistent styling across commands

Error Handling
--------------

Common error patterns and their meanings:

**"Habit 'name' not found"**
  The specified habit doesn't exist. Check spelling with ``gg list``.

**"Habit 'name' already exists"**
  Cannot create duplicate habit names. Use a different name.

**"Habit 'name' has already been completed today"**
  Daily habits can only be completed once per calendar day.

**"Invalid periodicity"**  
  Must be exactly "daily" or "weekly".

**"Database error"**
  Rare database corruption. Try removing ``~/.config/grit-guardian/habits.db`` and running ``gg init``.

Performance Notes
-----------------

- All commands execute in <100ms for typical usage
- Database operations are optimized for small datasets (<1000 habits)
- No network access required - all data stored locally
- Memory usage scales linearly with number of habits and completions
