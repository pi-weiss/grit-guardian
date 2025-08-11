Quick Start Guide
=================

This guide will get you up and running with Grit Guardian in 5 minutes.

Installation
------------

First, install Grit Guardian:

.. code-block:: bash

   pip install grit-guardian

Initialize with Sample Data
---------------------------

Start with pre-configured habits:

.. code-block:: bash

   gg init

This creates four sample habits:
- Morning Reading (daily)
- Exercise (daily) 
- Weekly Planning (weekly)
- Learn Something New (daily)

Basic Commands
--------------

List Your Habits
~~~~~~~~~~~~~~~~~

.. code-block:: bash

   gg list

Check Today's Status
~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   gg status

Complete a Habit
~~~~~~~~~~~~~~~~~

.. code-block:: bash

   gg complete "Morning Reading"

Meet Your Pet
~~~~~~~~~~~~~

.. code-block:: bash

   gg pet

Your First Week
---------------

Day 1-3: Getting Started
~~~~~~~~~~~~~~~~~~~~~~~~

1. **Complete some habits**:

   .. code-block:: bash

      gg complete "Morning Reading"
      gg complete "Exercise"

2. **Check your progress**:

   .. code-block:: bash

      gg status
      gg streaks

3. **Visit your pet**:

   .. code-block:: bash

      gg pet

Day 4-7: Building Streaks
~~~~~~~~~~~~~~~~~~~~~~~~~

1. **View weekly progress**:

   .. code-block:: bash

      gg weekly

2. **Check for struggling habits**:

   .. code-block:: bash

      gg struggled

3. **Add your own habit**:

   .. code-block:: bash

      gg add "Meditation" "10 minutes of mindfulness" daily

Essential Commands Reference
----------------------------

Habit Management
~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Add a new habit
   gg add "Habit Name" "Description" daily
   gg add "Weekly Review" "Plan the week" weekly

   # List all habits
   gg list

   # Delete a habit (with confirmation)
   gg delete "Habit Name"

Tracking Progress
~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Mark habit as complete
   gg complete "Habit Name"

   # View today's status
   gg status

   # See all streaks and completion rates
   gg streaks

Analytics & Insights
~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Weekly progress table
   gg weekly

   # Identify struggling habits
   gg struggled

   # Visit your Guardian pet
   gg pet

Sample Workflow
---------------

Here's a typical daily routine with Grit Guardian:

**Morning**:

.. code-block:: bash

   # Check what needs to be done today
   gg status

   # Complete morning habits
   gg complete "Morning Reading"

**Throughout the day**:

.. code-block:: bash

   # Complete habits as you do them
   gg complete "Exercise"

**Evening**:

.. code-block:: bash

   # Review your progress
   gg status
   gg pet

**Weekly review**:

.. code-block:: bash

   # See weekly progress
   gg weekly
   
   # Check for habits needing attention
   gg struggled
   
   # Complete weekly planning
   gg complete "Weekly Planning"

Tips for Success
----------------

1. **Start Small**: Begin with 2-3 easy habits
2. **Be Consistent**: Check in daily, even if briefly
3. **Use Your Pet**: Let your Guardian's mood motivate you
4. **Weekly Reviews**: Use ``gg weekly`` to identify patterns
5. **Don't Forget**: Use ``gg struggled`` to catch habits you're neglecting

Next Steps
----------

- Read the full :doc:`user_guide` for advanced features
- Check the :doc:`cli_reference` for all available commands
- Learn about :doc:`development/architecture` if you want to contribute

Need Help?
----------

- Use ``gg --help`` or ``gg [command] --help`` for command help
- Check the :doc:`user_guide` for detailed explanations
- Visit our `GitHub Issues <https://github.com/pi-weiss/grit-guardian/issues>`_ for support
