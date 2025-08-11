# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys

# Add the project directory to the Python path for autodoc
sys.path.insert(0, os.path.abspath("../.."))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "Grit Guardian"
copyright = "2025, Patrick Weiss"
author = "Patrick Weiss"
release = "1.0.0"
version = "1.0.0"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",  # For docstrings support
    "sphinx.ext.coverage",  # For auto-generating API documentation
    "sphinx.ext.napoleon",  # Pre-processing NumPy and Google style docstrings
    "sphinx.ext.viewcode",  # For adding links to highlighted source code
    "sphinx_copybutton",  # For adding a "copy" button to the right of code blocks
    "sphinxcontrib.mermaid",  # For embedding Mermaid graphs into the documentation
    "sphinx.ext.intersphinx",
    "sphinx.ext.autosummary",
]

# Napoleon settings for Google/NumPy style docstrings
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_type_aliases = None

# Autodoc settings
autodoc_default_options = {
    "members": True,
    "member-order": "bysource",
    "special-members": "__init__",
    "undoc-members": True,
    "exclude-members": "__weakref__",
}

# Autosummary settings
autosummary_generate = True
autosummary_imported_members = False

# Intersphinx mapping
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "click": ("https://click.palletsprojects.com/en/latest/", None),
}

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

language = "en"

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_theme_options = {
    "navigation_depth": 4,
    "collapse_navigation": False,
    "sticky_navigation": True,
    "includehidden": True,
    "titles_only": False,
    "logo_only": False,
    "prev_next_buttons_location": "both",
    "style_external_links": True,
}

html_static_path = ["_static"]
html_css_files = []

# Add custom CSS if it exists
if os.path.exists(os.path.join(os.path.dirname(__file__), "_static", "custom.css")):
    html_css_files.append("custom.css")

# Logo and favicon
html_logo = None
html_favicon = None

# Additional HTML options
html_show_sourcelink = True
html_show_sphinx = True
html_show_copyright = True
html_last_updated_fmt = "%b %d, %Y"

# -- Options for LaTeX output ------------------------------------------------
latex_elements = {
    "papersize": "letterpaper",
    "pointsize": "10pt",
    "preamble": "",
    "fncychap": "",
    "maketitle": "",
}

latex_documents = [
    ("index", "grit-guardian.tex", "Grit Guardian Documentation", "Team", "manual"),
]

# -- Options for manual page output ------------------------------------------
man_pages = [("index", "grit-guardian", "Grit Guardian Documentation", [author], 1)]

# -- Options for Texinfo output ----------------------------------------------
texinfo_documents = [
    (
        "index",
        "grit-guardian",
        "Grit Guardian Documentation",
        author,
        "grit-guardian",
        "Terminal-based habit tracker with virtual pet.",
        "Miscellaneous",
    ),
]

# -- Options for Epub output -------------------------------------------------
epub_title = project
epub_author = author
epub_publisher = author
epub_copyright = copyright
epub_exclude_files = ["search.html"]
# mermaid_output_format = 'png'
