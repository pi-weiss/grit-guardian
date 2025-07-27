import os
import sys

sys.path.insert(
    0, os.path.abspath("../..")
)  # Add the project directory to the Python path for autodoc

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "Grit Guardian"
copyright = "2025, Patrick Weiss"
author = "Patrick Weiss"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",  # For docstrings support
    "sphinx.ext.napoleon",  # Pre-processing NumPy and Google style docstrings
    "sphinx.ext.viewcode",  # For adding links to highlighted source code
    "sphinx_copybutton",  # For adding a "copy" button to the right of code blocks
    "sphinxcontrib.mermaid",  # For embedding Mermaid graphs into the documentation
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "alabaster"
html_static_path = ["_static"]
# mermaid_output_format = 'png'
