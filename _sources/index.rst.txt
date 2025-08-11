Grit Guardian Documentation
===========================

**CLI habit tracker with virtual companion** 🐉

Grit Guardian is a command-line habit tracking application that gamifies your daily and weekly routines with an interactive virtual companion (Guardian). Your Guardian's mood reflects your habit consistency, providing motivation to maintain streaks and build lasting habits.

.. image:: https://img.shields.io/badge/python-3.11+-blue.svg
   :target: https://www.python.org/downloads/
   :alt: Python 3.11+

.. image:: https://img.shields.io/badge/License-MIT-yellow.svg
   :target: https://opensource.org/licenses/MIT
   :alt: MIT License

Features
--------

* 📊 **Habit Tracking**: Track daily and weekly habits with completion timestamps
* 🔥 **Streak Analytics**: Calculate current and longest streaks with completion rates  
* 🐉 **Virtual Companion**: Interactive Guardian with mood based on your performance
* 📅 **Weekly Progress**: ASCII table showing week-at-a-glance habit completion
* 📈 **Analytics Dashboard**: Identify struggling habits and track overall progress
* 🎯 **Sample Data**: Quick-start with pre-configured habit examples
* 💾 **Local Storage**: SQLite database with automatic backup and recovery
* 🎨 **Beautiful CLI**: Colorful, emoji-rich interface with clear visual feedback

Quick Start
-----------

Install Grit Guardian and get started in minutes:

.. code-block:: bash

   pip install grit-guardian
   gg init
   gg status
   gg complete "Morning Reading"
   gg pet

Documentation Contents
----------------------

.. toctree::
   :maxdepth: 2
   :caption: User Guide:

   installation
   quickstart
   user_guide
   cli_reference

.. toctree::
   :maxdepth: 2
   :caption: API Reference:

   api/modules

.. toctree::
   :maxdepth: 2
   :caption: Development:

   development/contributing
   development/architecture

Community & Support
-------------------

* **Issues**: `GitHub Issues <https://github.com/pi-weiss/grit-guardian/issues>`_
* **Source Code**: `GitHub Repository <https://github.com/pi-weiss/grit-guardian>`_

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
