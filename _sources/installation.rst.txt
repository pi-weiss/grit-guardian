Installation
============

Requirements
------------

* Python 3.11 or higher
* Operating System: Linux, macOS, or Windows

Installation Methods
--------------------

From PyPI (Recommended)
~~~~~~~~~~~~~~~~~~~~~~~

Install the latest stable version from PyPI:

.. code-block:: bash

   pip install grit-guardian

This will install both the ``grit-guardian`` and ``gg`` commands.

From Source
~~~~~~~~~~~

For development or to get the latest features:

.. code-block:: bash

   git clone https://github.com/pi-weiss/grit-guardian.git
   cd grit-guardian
   pip install poetry  # If you don't have Poetry installed
   poetry install
   poetry shell

Verify Installation
-------------------

Check that the installation was successful:

.. code-block:: bash

   grit-guardian --help
   # or
   gg --help

You should see the main help message with available commands.

First Run
---------

Initialize Grit Guardian with sample data:

.. code-block:: bash

   gg init

This creates sample habits and shows you how to get started.

Upgrading
---------

To upgrade to the latest version:

.. code-block:: bash

   pip install --upgrade grit-guardian

Uninstallation
--------------

To remove Grit Guardian:

.. code-block:: bash

   pip uninstall grit-guardian

Note: This will not remove your habit data, which is stored in ``~/.config/grit-guardian/``.

Troubleshooting
---------------

Common Issues
~~~~~~~~~~~~~

**Permission Errors**
   If you encounter permission errors during installation, try:

   .. code-block:: bash

      pip install --user grit-guardian

**Command Not Found**
   If the ``gg`` command is not found after installation, ensure your Python scripts directory is in your PATH.

**Database Issues**
   If you have database problems, you can reset your data:

   .. code-block:: bash

      rm -rf ~/.config/grit-guardian/
      gg init

   **Warning**: This will delete all your habit data.

Getting Help
~~~~~~~~~~~~

If you encounter issues:

1. Check the `troubleshooting guide <https://github.com/pi-weiss/grit-guardian/issues>`_
2. Search existing `GitHub issues <https://github.com/pi-weiss/grit-guardian/issues>`_
3. Create a new issue with details about your system and the error
